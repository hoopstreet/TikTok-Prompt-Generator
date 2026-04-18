import os
import torch
import gradio as gr
from hf_moondream import HfMoondream

# FORCE OFFLINE MODE (PREVENT HF DOWNLOAD CRASH)
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

# LOCAL MODEL ONLY
model_path = "./moondream3"

model = HfMoondream.from_pretrained(
    model_path,
    local_files_only=True,
    trust_remote_code=True
)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
model.eval()

def generate_tiktok_hook(image, tone):
    if image is None:
        return "Upload product image first"

    if tone == "Budol (Aggressive)":
        prompt = "Describe this product as viral budol TikTok find. Taglish style."
    else:
        prompt = "Give short relatable Taglish TikTok review."

    result = model.query(image=image, question=prompt)
    return result["answer"]

with gr.Blocks() as demo:
    gr.Markdown("# TikTok Prompt Generator (LOCAL MOONDREAM 3)")
    
    img = gr.Image(type="pil")
    tone = gr.Radio(["Budol (Aggressive)", "Relatable"], value="Budol (Aggressive)")
    btn = gr.Button("Generate")
    out = gr.Textbox()

    btn.click(generate_tiktok_hook, inputs=[img, tone], outputs=out)

demo.launch(server_name="0.0.0.0", server_port=7860)
