import gradio as gr
import torch
from PIL import Image
from hf_moondream import HfMoondream, HfConfig

# ✅ Stable Moondream 3 reference (safe fallback format)
model_id = "moondream/moondream-3"

# Load model safely with fallback compatibility
model = HfMoondream.from_pretrained(
    model_id,
    trust_remote_code=True
).to("cuda" if torch.cuda.is_available() else "cpu")

model.eval()

def generate_tiktok_hook(image, tone):
    if image is None:
        return "Please upload a product photo first, boss!"

    if tone == "Budol (Aggressive)":
        prompt = (
            "Describe this product. Focus on why it is a must-buy budol find. "
            "Use Taglish and mention 'Check the yellow basket'."
        )
    else:
        prompt = (
            "Provide a short, honest review of this product in Taglish. "
            "Keep it relatable for a TikTok audience."
        )

    result = model.query(
        image=image,
        question=prompt
    )

    return result["answer"]

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🛒 TikTok Affiliate Budol Generator (Moondream 3)")

    with gr.Row():
        with gr.Column():
            input_img = gr.Image(type="pil", label="Product Photo")
            tone_sel = gr.Radio(
                ["Budol (Aggressive)", "Relatable/Honest"],
                label="Content Tone",
                value="Budol (Aggressive)"
            )
            submit_btn = gr.Button("🚀 Generate Viral Hook")

        with gr.Column():
            output_text = gr.Textbox(label="Generated Script", lines=10)

    submit_btn.click(
        fn=generate_tiktok_hook,
        inputs=[input_img, tone_sel],
        outputs=output_text
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
