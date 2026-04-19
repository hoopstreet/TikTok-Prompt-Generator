import gradio as gr
import random
import re
import requests
from PIL import Image
from io import BytesIO

class TikTokProductGenerator:
    def __init__(self):
        self.durations = [15, 30, 45]
        self.shot_counts = {15: 5, 30: 10, 45: 15}

    def detect_niche(self, title, about, description):
        text = (title + " " + about + " " + description).lower()
        niches = {
            "audio": ["earbuds", "headphones", "speaker", "bass", "wireless"],
            "apparel": ["shirt", "pants", "hoodie", "dress", "fabric"],
            "gaming": ["gaming", "mouse", "keyboard", "rgb", "controller"],
            "tech": ["charger", "powerbank", "cable", "adapter", "usb"],
            "motor": ["car", "motorcycle", "helmet", "tire", "oil"],
            "home": ["lamp", "organizer", "storage", "kitchen", "furniture"],
            "beauty": ["skincare", "makeup", "cream", "lotions", "serum"]
        }
        for niche, keywords in niches.items():
            if any(k in text for k in keywords):
                return niche
        return "general"

    def analyze_image_url(self, image_url):
        if not image_url:
            return "No image provided"
        try:
            if "ibyteimg.com" in image_url:
                return "ByteDance CDN image detected - valid"
            response = requests.head(image_url, timeout=5)
            if response.status_code == 200:
                return "Image URL valid"
            else:
                return "Image URL may be invalid"
        except:
            return "Cannot verify image URL"

    def generate_taglish_script(self, niche, duration, product_name):
        shots = self.shot_counts[duration]
        scripts = []
        taglish_lines = [
            ("Grabe ang ganda nito!", "Amazing quality"),
            ("Solid ang quality mga idol!", "Great quality"),
            ("Sulit na sulit sa presyo!", "Very worth it"),
            ("Kunin niyo na yung sa'yo!", "Get yours now"),
            ("Kailangan niyo to!", "You need this"),
            ("Swerte niyo mga idol!", "You are lucky"),
            ("Panalo to mga boss!", "This is a winner"),
            ("Mura pero quality!", "Cheap but quality")
        ]
        movements = ["Cinematic Pan", "Dynamic Zoom-in", "Handheld POV", "Slow-motion"]
        lighting = ["Soft Studio", "Natural Sunlight", "Neon Glow"]
        for i in range(shots):
            taglish, eng = taglish_lines[i % len(taglish_lines)]
            mov = movements[i % len(movements)]
            lit = lighting[i % len(lighting)]
            scripts.append(f"Shot {i+1:02d} (3s): 4K vertical 9:16 [{mov}] [{lit}] {taglish}")
        return scripts

    def generate(self, product_title, about_this_product, product_description, image_url):
        niche = self.detect_niche(product_title, about_this_product, product_description)
        duration = random.choice(self.durations)
        shots = self.shot_counts[duration]
        scripts = self.generate_taglish_script(niche, duration, product_title)
        image_status = self.analyze_image_url(image_url)
        positive = ""
        for s in scripts:
            positive += s + "\n"
        negative = "low quality, blurry, distorted, glitch, color bleed, watermark, low resolution, messy textures, robotic voice, formal language, text overlap, no motion blur, no frame tearing"
        final_title = f"🔥 MUST-HAVE! {product_title[:50]} | {niche.upper()} Finds #TikTokMadeMeBuyIt #BudolFinds #Sulit #Quality #Affiliate"
        output = f"""
================================================================================
FINAL OUTPUT - COLUMN MAPPING
================================================================================

Column: positive_prompt

{positive}

================================================================================

Column: negative_prompt

{negative}

================================================================================

Column: final_title

{final_title}

================================================================================

System Name: TikTok-Product-Generator-V1
DNA-Signature: HOOPSTREET-AFFILIATE-LOGIC-2026
Detected Niche: {niche}
Region: PH-LOCALIZED
Duration: {duration}s
Shots: {shots}
Image Status: {image_status}

================================================================================
"""
        return output

generator = TikTokProductGenerator()

with gr.Blocks(title="TikTok Product Generator", theme="soft") as demo:
    gr.Markdown("# TikTok Product Generator")
    gr.Markdown("Generate TikTok affiliate content - Philippines Market")

    with gr.Row():
        with gr.Column(scale=1):
            product_title = gr.Textbox(label="Product Title", placeholder="Enter product name")
            about_this_product = gr.Textbox(label="About This Product", lines=2)
            product_description = gr.Textbox(label="Product Description", lines=3)
            image_url = gr.Textbox(label="Image URL", placeholder="https://...")
            submit = gr.Button("Generate", variant="primary")

        with gr.Column(scale=1):
            output = gr.Textbox(label="Generated Output", lines=30)

    submit.click(
        fn=generator.generate,
        inputs=[product_title, about_this_product, product_description, image_url],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
