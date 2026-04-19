import gradio as gr
import random
import re
import requests
import json
from PIL import Image
from io import BytesIO
from datetime import datetime

class TikTokProductGenerator:
    def __init__(self):
        self.durations = [15, 30, 45]
        self.shot_counts = {15: 5, 30: 10, 45: 15}
        self.history = []

    def detect_niche(self, title, about, description):
        text = (title + " " + about + " " + description).lower()
        niches = {
            "apparel": ["shirt", "pants", "hoodie", "dress", "fabric", "shorts", "athletic"],
            "audio": ["earbuds", "headphones", "speaker", "bass", "wireless"],
            "gaming": ["gaming", "mouse", "keyboard", "rgb", "controller"],
            "tech": ["charger", "powerbank", "cable", "adapter", "usb"],
            "motor": ["car", "motorcycle", "helmet", "tire", "oil"],
            "home": ["lamp", "organizer", "storage", "kitchen", "furniture"],
            "beauty": ["skincare", "makeup", "cream", "lotions", "serum"],
            "sports": ["basketball", "mesh", "jersey", "shorts", "athletic"],
            "tools": ["heavy-duty", "rechargeable", "cordless", "handy"]
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
                return "ByteDance CDN detected - valid TikTok Shop image"
            if "resize-webp" in image_url:
                return "WebP format detected - optimized for mobile"
            response = requests.head(image_url, timeout=5)
            if response.status_code == 200:
                return "Image URL valid"
            else:
                return "Image URL may be invalid"
        except:
            return "Cannot verify image URL - will still process"

    def generate_product_card(self, title, niche, features):
        return f"""
[PRODUCT INFO CARD]
Product Name: {title}
Category: {niche.upper()}
Key Features: {features}
"""

    def generate_video_brief_card(self, niche, duration, audience):
        shots = self.shot_counts[duration]
        return f"""
[VIDEO BRIEF CARD]
Niche: {niche}
Duration: {duration} seconds
Shot Count: {shots} shots
Target Audience: {audience}
Mood: Energetic, Budol vibe
"""

    def generate_analysis_card(self, duration, shots):
        return f"""
[VIDEO ANALYSIS RESULTS]
Total Shots: {shots}
Audio Style: Taglish voiceover + Upbeat music
Lighting Guide: Natural/Studio/Neon
Resolution: 4K Vertical 9:16
Duration: {duration}s (3s per shot rule)
"""

    def generate_storyboard_card(self, niche, duration, product_name):
        shots = self.shot_counts[duration]
        storyboard = "\n[VIDEO STORYBOARD CARD]\n"
        taglish_lines = [
            ("Apat na bagong kulay, grabe!", "Four new colors, amazing!"),
            ("Solid ang quality mga idol!", "Quality is solid guys!"),
            ("Sulit na sulit sa presyo!", "Very worth it for the price!"),
            ("Kunin niyo na yung sa'yo!", "Get yours now!"),
            ("Stretchy lightweight fabric, presko!", "Stretchy lightweight fabric, breathable!"),
            ("Double-lined kaya makapal ang tela!", "Double-lined so the fabric is thick!"),
            ("May bulsa sa magkabilang gilid!", "Has pockets on both sides!"),
            ("Assorted colors, sulit na bundle!", "Assorted colors, worth it bundle!")
        ]
        movements = ["Cinematic Pan", "Dynamic Zoom-in", "Handheld POV", "Slow-motion reveal"]
        lighting = ["Soft Studio Lighting", "Natural Sunlight", "Neon Glow"]
        for i in range(shots):
            taglish, eng = taglish_lines[i % len(taglish_lines)]
            mov = movements[i % len(movements)]
            lit = lighting[i % len(lighting)]
            storyboard += f"Shot {i+1:02d} ({duration/shots:.1f}s): [{mov}] [{lit}] {taglish}\n"
        return storyboard

    def generate(self, product_title, about_this_product, product_description, image_url):
        niche = self.detect_niche(product_title, about_this_product, product_description)
        duration = random.choice(self.durations)
        shots = self.shot_counts[duration]
        features = product_description[:100] if product_description else "Premium quality product"
        audience = "Fitness enthusiasts" if niche == "apparel" else "General TikTok users"
        image_status = self.analyze_image_url(image_url)
        product_card = self.generate_product_card(product_title, niche, features)
        brief_card = self.generate_video_brief_card(niche, duration, audience)
        analysis_card = self.generate_analysis_card(duration, shots)
        storyboard_card = self.generate_storyboard_card(niche, duration, product_title)
        scripts = self.generate_storyboard_card(niche, duration, product_title)
        positive = ""
        for line in scripts.split("\n"):
            if "Shot" in line:
                positive += line + "\n"
        negative = "low quality, blurry, distorted, glitch, color bleed, watermark, low resolution, messy textures, robotic voice, formal language, text overlap, no motion blur, no frame tearing, do not change logo position, do not alter fabric color"
        final_title = f"🔥 MUST-HAVE! {product_title[:50]} | {niche.upper()} Finds #TikTokMadeMeBuyIt #BudolFinds #Sulit #Quality #Affiliate"
        
        output = f"""
================================================================================
FINAL OUTPUT - COLUMN MAPPING
================================================================================
{product_card}
{brief_card}
{analysis_card}
{storyboard_card}
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
Generation Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

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
            output = gr.Textbox(label="Generated Output", lines=35)
    
    submit.click(
        fn=generator.generate,
        inputs=[product_title, about_this_product, product_description, image_url],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
