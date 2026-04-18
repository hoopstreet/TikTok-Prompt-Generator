import os
import torch
import gradio as gr
from hf_moondream import HfMoondream

# -------------------------
# SAFE MODE (NO HF CALLS)
# -------------------------
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

# -------------------------
# LOAD FROM REPO ROOT (FIX)
# -------------------------
model = HfMoondream.from_pretrained(
    ".",   # ✅ THIS IS THE FIX (NOT moondream3)
    local_files_only=True,
    trust_remote_code=True,
    use_safetensors=True
)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
model.eval()

# -------------------------
# CORE FUNCTION
# -------------------------
def generate_tiktok_hook(image, tone):
    if image is None:
        return "Upload product image first"

    if tone == "Budol (Aggressive)":
        prompt = (
            "Describe this product as a viral budol TikTok find. "
            "Use Taglish. Make it persuasive and hype."
        )
    else:
        prompt = (
            "Give a short relatable TikTok-style Taglish review."
        )

    result = model.query(image=image, question=prompt)
    return result["answer"]

# -------------------------
# UI
# -------------------------
with gr.Blocks() as demo:
    gr.Markdown("# 🛒 TikTok Prompt Generator (HF STABLE MODE)")

    with gr.Row():
        img = gr.Image(type="pil")
        tone = gr.Radio(
            ["Budol (Aggressive)", "Relatable"],
            value="Budol (Aggressive)"
        )

    btn = gr.Button("Generate")
    out = gr.Textbox()

    btn.click(generate_tiktok_hook, inputs=[img, tone], outputs=out)

demo.launch(server_name="0.0.0.0", server_port=7860)
