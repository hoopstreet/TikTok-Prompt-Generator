import gradio as gr
from model_loader import MoondreamLoader
from prompt_templates import TikTokPrompt
from output_parser import TikTokOutputParser

def analyze_product(title, description, product_details, image_url, custom_instruction):
    prompt = TikTokPrompt.build(title, description, product_details, custom_instruction)
    
    response = f"""Hook: {title[:50]} will change your life!
Problem Solved: Solves {description[:50]}...
Emotional Angle: You deserve this solution
Call to Action: Click link in bio
Hashtags: #TikTokMadeMeBuyIt #Viral #Trending #ProductReview #MustHave"""
    
    formatted = TikTokOutputParser.parse(response)
    return formatted

with gr.Blocks(title="TikTok Prompt Generator", theme="soft") as demo:
    gr.Markdown("# TikTok Prompt Generator")
    gr.Markdown("Generate viral TikTok content using AI")
    
    with gr.Row():
        with gr.Column(scale=1):
            title = gr.Textbox(label="Product Title", placeholder="Enter product name...")
            description = gr.Textbox(label="Product Description", lines=3)
            product_details = gr.Textbox(label="Additional Details", lines=2)
            image_url = gr.Textbox(label="Image URL", placeholder="https://...")
            custom = gr.Textbox(label="Custom Instructions (optional)", lines=2)
            submit = gr.Button("Generate Prompt", variant="primary")
        
        with gr.Column(scale=1):
            output = gr.Textbox(label="Generated TikTok Prompt", lines=15)
    
    submit.click(
        fn=analyze_product,
        inputs=[title, description, product_details, image_url, custom],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
