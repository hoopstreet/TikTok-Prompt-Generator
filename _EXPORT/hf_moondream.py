import torch
import torch.nn as nn
import gradio as gr
from transformers import PreTrainedModel, PretrainedConfig, AutoTokenizer
from typing import Union
from PIL import Image

# FIXED: Changed relative imports to absolute for Docker compatibility
from config import MoondreamConfig
from moondream import MoondreamModel
from image_crops import *
from vision import *
from text import *
from region import *
from utils import *

def extract_question(text):
    prefix = "<image>\n\nQuestion: "
    suffix = "\n\nAnswer:"
    if text.startswith(prefix) and text.endswith(suffix):
        return text[len(prefix) : -len(suffix)]
    return None

class HfConfig(PretrainedConfig):
    _auto_class = "AutoConfig"
    model_type = "moondream3"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = {"skills": ["query", "caption", "detect", "point"]}

class HfMoondream(PreTrainedModel):
    _auto_class = "AutoModelForCausalLM"
    config_class = HfConfig
    def __init__(self, config):
        super().__init__(config)
        self.model = MoondreamModel(MoondreamConfig.from_dict(config.config), setup_caches=False)
        self._is_kv_cache_setup = False
        self.post_init()

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        output = super().from_pretrained(*args, **kwargs)
        model = output[0] if isinstance(output, tuple) else output
        model.model._refresh_runtime_buffers()
        return output

    def _setup_caches(self):
        if not self._is_kv_cache_setup:
            self.model._setup_caches()
            self._is_kv_cache_setup = True

    def query(self, image, question):
        self._setup_caches()
        return self.model.query(image, question)

# --- GRADIO INTERFACE LOGIC ---

def generate_tiktok_script(image):
    if image is None:
        return "Hoy! Mag-upload ka muna ng image. (Upload an image first!)"
    
    # Initialize model (points to current directory weights)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = HfMoondream.from_pretrained(".")
    
    # Analyze Image
    description = model.query(image, "Describe this product's aesthetic and key selling points.")["answer"]
    
    # Taglish Marketing Framework
    taglish_script = f"""
🚀 TIKTOK VIRAL DNA SCRIPT
--------------------------
🪝 HOOK (0-3s):
"Grabe guys, hindi niyo aakalain 'to! Check out this product..."

📦 BODY (3-10s):
"Sobrang solid ng features nito. Very aesthetic and perfect for your daily grind. 
Detailed features: {description}"

🔥 CALL TO ACTION (10-15s):
"Kaya wag na kayong mag-pahuli. Click the yellow basket and check out na! 
Budol find of the day! ✨ #TikTokFinds #BudolPH #TaglishAds"
    """
    return taglish_script

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🧬 TikTok Taglish Prompt Generator (v1.1.1)")
    with gr.Row():
        with gr.Column():
            input_img = gr.Image(type="pil", label="Product Image")
            generate_btn = gr.Button("Generate Taglish DNA", variant="primary")
        with gr.Column():
            output_text = gr.Textbox(label="TikTok Script (Taglish)", lines=12)
    generate_btn.click(generate_tiktok_script, inputs=input_img, outputs=output_text)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
