---
library_name: transformers
tags: []
---

Moondream 3 (Preview) is vision language model with a mixture of experts architecture (9B total parameters, 2B active).

Architecture details:

1. 24 layers; the first four are dense, the rest have MoE FFNs with 64 experts, 8 activated per token
2. MoE FFNs have GeGLU architecture, with inner/gate dim of 1024. The model's hidden dim is 2048.
3. Usable context length increased to 32K, with [a custom efficient SuperBPE tokenizer](https://huggingface.co/moondream/starmie-v1)
4. Multi-headed attention with learned position- and data-dependent temperature scaling
5. Vision encoder initialized from SigLIP-SO-400M, with multi-crop channel concatenation for token-efficient high resolution image processing

For more details, please refer to our ||coming soon release blog post||.