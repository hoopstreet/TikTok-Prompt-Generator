import gradio as gr
from model_loader import MoondreamLoader
from prompt_templates import TikTokPrompt
from output_parser import TikTokOutputParser

# Initialize model loader (downloads weights on first run)
loader = MoondreamLoader(model_id="hoopstreet/moondream3-preview")
model = loader.load_model()

def analyze_tiktok_product(title, description, product_details, image_url, custom_instruction):
    """
    Custom function that takes your input fields and returns formatted output
    """
    # Load and process image from URL
    image = loader.load_image_from_url(image_url)
    
    # Build prompt using your template
    prompt = TikTokPrompt.build(
        title=title,
        description=description,
        product_details=product_details,
        custom_instruction=custom_instruction
    )
    
    # Run inference
    response = model.answer_question(image, prompt)
    
    # Parse and format output
    formatted_output = TikTokOutputParser.parse(response)
    
    return formatted_output

# Create custom UI with your input fields
with gr.Blocks(title="TikTok Prompt Generator") as demo:
    gr.Markdown("# TikTok Product Analysis")
    
    with gr.Row():
        with gr.Column():
            title = gr.Textbox(label="Product Title", placeholder="Enter product title...")
            description = gr.Textbox(label="Product Description", lines=3)
            product_details = gr.Textbox(label="Additional Product Details", lines=2)
            image_url = gr.Textbox(label="Product Image URL", placeholder="https://...")
            custom_instruction = gr.Textbox(label="Custom Instruction (Optional)", lines=2)
            submit_btn = gr.Button("Generate TikTok Prompt")
        
        with gr.Column():
            output = gr.Textbox(label="Generated Output", lines=10)
    
    submit_btn.click(
        fn=analyze_tiktok_product,
        inputs=[title, description, product_details, image_url, custom_instruction],
        outputs=output
    )

demo.launch(server_name="0.0.0.0", server_port=7860)
