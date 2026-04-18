import os
import torch
import gradio as gr
from hf_moondream import HfMoondream

# =========================
# FORCE SAFE OFFLINE MODE
# =========================
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

# =========================
# ABSOLUTE LOCAL PATH FIX
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "moondream3")

# =========================
# LOAD MODEL SAFELY
# =========================
model = HfMoondream.from_pretrained(
    model_path,
    local_files_only=True,
    trust_remote_code=False,  # IMPORTANT FIX
)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
model.eval()

# =========================
# CORE FUNCTION
# =========================
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

    return result.get("answer", str(result))

# =========================
# UI
# =========================
with gr.Blocks() as demo:
    gr.Markdown("# 🛒 TikTok Prompt Generator (Moondream LOCAL SAFE MODE)")

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
