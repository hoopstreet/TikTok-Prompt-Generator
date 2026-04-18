import gradio as gr
import torch
from PIL import Image
from hf_moondream import HfMoondream

# ✅ LOCAL REPO MODEL ONLY (NO HF HUB DOWNLOAD)
model = HfMoondream.from_pretrained(
    "./",   # <-- IMPORTANT: use local repo weights
    trust_remote_code=True,
    local_files_only=True
)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
model.eval()

def generate_tiktok_hook(image, tone):
    if image is None:
        return "Upload product image first"

    if tone == "Budol (Aggressive)":
        prompt = "Describe this product as a viral budol TikTok find. Taglish. Mention yellow basket."
    else:
        prompt = "Give a relatable short Taglish review for TikTok."

    result = model.query(image=image, question=prompt)
    return result["answer"]

with gr.Blocks() as demo:
    gr.Markdown("# TikTok Prompt Generator (Moondream LOCAL MODE)")

    with gr.Row():
        img = gr.Image(type="pil")
        tone = gr.Radio(["Budol (Aggressive)", "Relatable"], value="Budol (Aggressive)")
        btn = gr.Button("Generate")

    out = gr.Textbox()

    btn.click(generate_tiktok_hook, inputs=[img, tone], outputs=out)

demo.launch(server_name="0.0.0.0", server_port=7860)
