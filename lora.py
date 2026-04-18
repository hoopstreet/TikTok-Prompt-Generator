import json
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from urllib.request import Request, urlopen

import torch

from config import TextConfig


class AdapterLoadError(RuntimeError):
    pass


def _cache_root() -> Path:
    hf_hub_cache = os.environ.get("HF_HUB_CACHE")
    if hf_hub_cache:
        return Path(hf_hub_cache)

    hf_home = os.environ.get("HF_HOME")
    if hf_home:
        return Path(hf_home) / "hub"

    return Path("~/.cache/huggingface/hub").expanduser()


def adapter_cache_dir() -> Path:
    return _cache_root() / "md_finetunes"


def normalize_adapter_id(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    tail = value.split("/")[-1].strip()
    if "@" not in tail:
        return None
    return tail


def parse_adapter_id(adapter_id: str) -> Tuple[str, str]:
    if not adapter_id or "@" not in adapter_id:
        raise AdapterLoadError(
            f"Invalid adapter id '{adapter_id}'. Expected 'finetune_id@step'."
        )
    finetune_id, step = adapter_id.split("@", 1)
    if not finetune_id or not step:
        raise AdapterLoadError(
            f"Invalid adapter id '{adapter_id}'. Expected 'finetune_id@step'."
        )
    return finetune_id, step


def _fetch_presigned_url(finetune_id: str, step: str) -> str:
    endpoint = os.getenv("MOONDREAM_ENDPOINT", "https://api.moondream.ai").rstrip("/")
    api_key = os.getenv("MOONDREAM_API_KEY")
    if not api_key:
        raise AdapterLoadError("MOONDREAM_API_KEY is required to load finetune adapters.")

    headers = {"User-Agent": "moondream-torch", "X-Moondream-Auth": api_key}
    url = f"{endpoint}/v1/tuning/finetunes/{finetune_id}/checkpoints/{step}/download"
    req = Request(url, headers=headers)
    try:
        with urlopen(req) as r:
            payload = json.loads(r.read().decode("utf-8"))
    except Exception as e:
        raise AdapterLoadError(f"Failed to fetch adapter URL: {e}") from e

    presigned = payload.get("url")
    if not presigned:
        raise AdapterLoadError("Adapter URL response missing 'url' field.")
    return presigned


def cached_adapter_path(adapter_id: str) -> Path:
    finetune_id, step = parse_adapter_id(adapter_id)

    cache_dir = adapter_cache_dir() / finetune_id / step
    cache_dir.mkdir(parents=True, exist_ok=True)

    for name in ("adapter.pt", "adapter.safetensors"):
        path = cache_dir / name
        if path.exists() and path.stat().st_size > 0:
            return path

    presigned_url = _fetch_presigned_url(finetune_id, step)
    dest = cache_dir / "adapter.pt"

    try:
        with urlopen(presigned_url) as r, open(dest, "wb") as f:
            shutil.copyfileobj(r, f)
    except Exception as e:
        raise AdapterLoadError(f"Failed to download adapter: {e}") from e
    return dest


def _load_state_dict(path: Path, device: torch.device) -> Dict[str, Any]:
    if path.suffix == ".safetensors":
        try:
            from safetensors.torch import safe_open
        except Exception as e:
            raise AdapterLoadError(
                "safetensors is required to load .safetensors adapters."
            ) from e
        data = {}
        with safe_open(str(path), framework="pt") as f:
            for key in f.keys():
                data[key] = f.get_tensor(key).to(device=device)
        return data

    try:
        return torch.load(path, map_location=device, weights_only=True)
    except TypeError:
        return torch.load(path, map_location=device)


@dataclass
class DenseLoRALayer:
    up_a: torch.Tensor
    up_b: torch.Tensor
    down_a: torch.Tensor
    down_b: torch.Tensor


@dataclass
class MoELoRALayer:
    up_a: torch.Tensor
    up_b: torch.Tensor
    down_a: torch.Tensor
    down_b: torch.Tensor


class TextLoRA:
    def __init__(
        self,
        text_config: TextConfig,
        *,
        rank: int,
        max_rank: int,
        dtype: torch.dtype,
        device: torch.device,
        adapter_id: Optional[str] = None,
    ) -> None:
        if rank <= 0:
            raise AdapterLoadError("LoRA rank must be positive.")
        if max_rank < rank:
            raise AdapterLoadError("max_rank must be >= rank.")

        self.text_config = text_config
        self.rank = rank
        self.max_rank = max_rank
        self.adapter_id = adapter_id

        moe_cfg = text_config.moe
        self.start_layer = moe_cfg.start_layer if moe_cfg else text_config.n_layers

        if moe_cfg is not None:
            self.rank_per_expert = rank // moe_cfg.experts_per_token
            if self.rank_per_expert < 1:
                raise AdapterLoadError(
                    f"rank ({rank}) must be >= experts_per_token ({moe_cfg.experts_per_token})"
                )
            self.max_rank_per_expert = max_rank // moe_cfg.experts_per_token
            if self.max_rank_per_expert < 1:
                raise AdapterLoadError(
                    f"max_rank ({max_rank}) must be >= experts_per_token ({moe_cfg.experts_per_token})"
                )
        else:
            self.rank_per_expert = 0
            self.max_rank_per_expert = 0

        d_model = text_config.dim
        d_ffn = text_config.ff_dim

        self.dense: list[DenseLoRALayer] = []
        for _ in range(self.start_layer):
            self.dense.append(
                DenseLoRALayer(
                    up_a=torch.zeros((max_rank, d_model), device=device, dtype=dtype),
                    up_b=torch.zeros((d_ffn, max_rank), device=device, dtype=dtype),
                    down_a=torch.zeros((max_rank, d_ffn), device=device, dtype=dtype),
                    down_b=torch.zeros((d_model, max_rank), device=device, dtype=dtype),
                )
            )

        self.moe: list[MoELoRALayer] = []
        if moe_cfg is not None:
            num_experts = moe_cfg.num_experts
            d_expert = moe_cfg.expert_inner_dim
            for _ in range(text_config.n_layers - self.start_layer):
                self.moe.append(
                    MoELoRALayer(
                        up_a=torch.zeros(
                            (num_experts, self.max_rank_per_expert, d_model),
                            device=device,
                            dtype=dtype,
                        ),
                        up_b=torch.zeros(
                            (num_experts, d_expert * 2, self.max_rank_per_expert),
                            device=device,
                            dtype=dtype,
                        ),
                        down_a=torch.zeros(
                            (num_experts, self.max_rank_per_expert, d_expert),
                            device=device,
                            dtype=dtype,
                        ),
                        down_b=torch.zeros(
                            (num_experts, d_model, self.max_rank_per_expert),
                            device=device,
                            dtype=dtype,
                        ),
                    )
                )

    def dense_layer(self, layer_idx: int) -> Optional[DenseLoRALayer]:
        if layer_idx < len(self.dense):
            return self.dense[layer_idx]
        return None

    def moe_layer(self, layer_idx: int) -> Optional[MoELoRALayer]:
        moe_idx = layer_idx - self.start_layer
        if 0 <= moe_idx < len(self.moe):
            return self.moe[moe_idx]
        return None

    @staticmethod
    def _pad_axis(tensor: torch.Tensor, target: int, axis: int) -> torch.Tensor:
        if tensor.shape[axis] == target:
            return tensor
        if tensor.shape[axis] > target:
            raise AdapterLoadError(
                f"LoRA tensor rank {tensor.shape[axis]} exceeds max {target}"
            )
        pad_shape = list(tensor.shape)
        pad_shape[axis] = target - tensor.shape[axis]
        pad = torch.zeros(pad_shape, device=tensor.device, dtype=tensor.dtype)
        return torch.cat([tensor, pad], dim=axis)

    @staticmethod
    def detect_rank(state_dict: Dict[str, Any], text_config: TextConfig) -> int:
        for key, tensor in state_dict.items():
            if "dense" in key and "up_a" in key:
                return int(tensor.shape[0])
        for key, tensor in state_dict.items():
            if "moe" in key and "up_a" in key:
                rank_per_expert = int(tensor.shape[1])
                moe_cfg = text_config.moe
                if moe_cfg:
                    return rank_per_expert * moe_cfg.experts_per_token
                return rank_per_expert
        raise AdapterLoadError("Could not detect LoRA rank from state dict.")

    @classmethod
    def from_state_dict(
        cls,
        state_dict: Dict[str, Any],
        *,
        text_config: TextConfig,
        max_rank: int,
        dtype: torch.dtype,
        device: torch.device,
        adapter_id: Optional[str] = None,
    ) -> "TextLoRA":
        rank = cls.detect_rank(state_dict, text_config)
        if rank > max_rank:
            raise AdapterLoadError(
                f"Adapter rank ({rank}) exceeds max_rank ({max_rank})."
            )

        lora = cls(
            text_config,
            rank=rank,
            max_rank=max_rank,
            dtype=dtype,
            device=device,
            adapter_id=adapter_id,
        )

        dense_seen = set()
        moe_seen = set()

        pattern = re.compile(r"(dense|moe)\.(\d+)\.(up_a|up_b|down_a|down_b)$")
        for key, tensor in state_dict.items():
            match = pattern.search(key)
            if not match:
                continue
            kind, idx_str, name = match.group(1), match.group(2), match.group(3)
            idx = int(idx_str)
            arr = tensor.to(device=device, dtype=dtype)

            if kind == "dense":
                if idx >= len(lora.dense):
                    raise AdapterLoadError(f"Dense LoRA layer index {idx} out of range.")
                layer = lora.dense[idx]
                if name in ("up_a", "down_a"):
                    arr = cls._pad_axis(arr, lora.max_rank, axis=0)
                else:
                    arr = cls._pad_axis(arr, lora.max_rank, axis=1)
                setattr(layer, name, arr)
                dense_seen.add((idx, name))
            else:
                if idx >= len(lora.moe):
                    raise AdapterLoadError(f"MoE LoRA layer index {idx} out of range.")
                layer = lora.moe[idx]
                if name in ("up_a", "down_a"):
                    arr = cls._pad_axis(arr, lora.max_rank_per_expert, axis=1)
                else:
                    arr = cls._pad_axis(arr, lora.max_rank_per_expert, axis=2)
                setattr(layer, name, arr)
                moe_seen.add((idx, name))

        for layer_idx in range(len(lora.dense)):
            for name in ("up_a", "up_b", "down_a", "down_b"):
                if (layer_idx, name) not in dense_seen:
                    raise AdapterLoadError(
                        f"Adapter missing dense LoRA for layer {layer_idx} ({name})."
                    )
        for layer_idx in range(len(lora.moe)):
            for name in ("up_a", "up_b", "down_a", "down_b"):
                if (layer_idx, name) not in moe_seen:
                    raise AdapterLoadError(
                        f"Adapter missing MoE LoRA for layer {layer_idx} ({name})."
                    )

        return lora


def select_layer_lora(
    lora: Optional[TextLoRA], layer_idx: int, *, is_moe: bool
) -> Optional[object]:
    if lora is None:
        return None
    return lora.moe_layer(layer_idx) if is_moe else lora.dense_layer(layer_idx)


def apply_dense_lora(
    x: torch.Tensor, lora_a: torch.Tensor, lora_b: torch.Tensor
) -> torch.Tensor:
    b, t, c = x.shape
    x_flat = x.reshape(-1, c)
    lora_mid = torch.matmul(x_flat, lora_a.t())
    lora_out = torch.matmul(lora_mid, lora_b.t())
    return lora_out.reshape(b, t, -1)


def apply_moe_lora_fc1_flat(
    x_expanded: torch.Tensor, lora: MoELoRALayer, flat_idxs: torch.Tensor
) -> torch.Tensor:
    lora_up_a = lora.up_a[flat_idxs]
    lora_up_b = lora.up_b[flat_idxs]
    lora_mid = torch.bmm(lora_up_a, x_expanded.unsqueeze(-1)).squeeze(-1)
    lora_up = torch.bmm(lora_up_b, lora_mid.unsqueeze(-1)).squeeze(-1)
    return lora_up


def apply_moe_lora_fc2_flat(
    h: torch.Tensor, lora: MoELoRALayer, flat_idxs: torch.Tensor
) -> torch.Tensor:
    lora_down_a = lora.down_a[flat_idxs]
    lora_down_b = lora.down_b[flat_idxs]
    lora_mid = torch.bmm(lora_down_a, h.unsqueeze(-1)).squeeze(-1)
    lora_down = torch.bmm(lora_down_b, lora_mid.unsqueeze(-1)).squeeze(-1)
    return lora_down


_ADAPTER_CACHE: Dict[Tuple[str, str, str, Tuple], TextLoRA] = {}
_CACHE_ORDER: list[Tuple[str, str, str, Tuple]] = []
_CACHE_SIZE = 8


def _config_key(text_config: TextConfig) -> Tuple:
    moe = text_config.moe
    moe_key = None
    if moe is not None:
        moe_key = (
            moe.num_experts,
            moe.start_layer,
            moe.experts_per_token,
            moe.expert_inner_dim,
        )
    return (
        text_config.dim,
        text_config.ff_dim,
        text_config.n_layers,
        moe_key,
    )


def load_adapter(
    adapter_id: Optional[str],
    *,
    text_config: TextConfig,
    device: torch.device,
    dtype: torch.dtype,
    max_rank: int = 16,
) -> Optional[TextLoRA]:
    if adapter_id is None:
        return None

    adapter_id = normalize_adapter_id(adapter_id)
    if adapter_id is None:
        return None

    key = (adapter_id, str(device), str(dtype), _config_key(text_config))
    cached = _ADAPTER_CACHE.get(key)
    if cached is not None:
        return cached

    path = cached_adapter_path(adapter_id)
    checkpoint = _load_state_dict(path, device)
    if not isinstance(checkpoint, dict):
        raise AdapterLoadError("Invalid adapter checkpoint format.")

    state_dict = checkpoint.get("lora_state_dict", checkpoint)
    if not isinstance(state_dict, dict):
        raise AdapterLoadError("Adapter checkpoint missing lora_state_dict.")

    lora = TextLoRA.from_state_dict(
        state_dict,
        text_config=text_config,
        max_rank=max_rank,
        dtype=dtype,
        device=device,
        adapter_id=adapter_id,
    )

    _ADAPTER_CACHE[key] = lora
    _CACHE_ORDER.append(key)
    if len(_CACHE_ORDER) > _CACHE_SIZE:
        old = _CACHE_ORDER.pop(0)
        _ADAPTER_CACHE.pop(old, None)

    return lora
