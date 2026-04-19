import gradio as gr
import random
import re
import requests
import json
import uuid
from datetime import datetime
from PIL import Image
from io import BytesIO

class TikTokProductGenerator:
    def __init__(self):
        self.durations = [15, 30, 45, 55]
        self.shot_counts = {15: 5, 30: 10, 45: 15, 55: 18}
        self.history = []
        self.conversation_id = str(uuid.uuid4())
        
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
            "sports": ["basketball", "mesh", "jersey", "sports"],
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
                return "ByteDance CDN valid"
            if "resize-webp" in image_url:
                return "WebP format optimized"
            response = requests.head(image_url, timeout=5)
            if response.status_code == 200:
                return "Image URL valid"
            else:
                return "Image URL may be invalid"
        except:
            return "Cannot verify - will process"

    def generate_positive_prompt(self, niche, duration, product_name, shots):
        scripts = []
        taglish_lines = [
            ("Grabe ang ganda nito!", "Close-up product"),
            ("Solid ang quality mga idol!", "Fabric texture"),
            ("Sulit na sulit sa presyo!", "Price tag reveal"),
            ("Kunin niyo na yung sa'yo!", "Yellow basket"),
            ("Kailangan niyo to!", "Problem solution"),
            ("Swerte niyo mga idol!", "Happy customer"),
            ("Panalo to mga boss!", "Winner celebration"),
            ("Mura pero quality!", "Price comparison")
        ]
        movements = ["Cinematic Pan", "Dynamic Zoom", "Handheld POV", "Slow-motion"]
        lighting = ["Soft Studio", "Natural Sunlight", "Neon Glow"]
        for i in range(shots):
            taglish, action = taglish_lines[i % len(taglish_lines)]
            mov = movements[i % len(movements)]
            lit = lighting[i % len(lighting)]
            scripts.append(f"Shot {i+1:02d} ({duration/shots:.1f}s): 4K vertical 9:16 [{mov}] [{lit}] {action} + Dialogue: {taglish}")
        return scripts

    def generate_negative_prompt(self, scripts):
        negatives = []
        movements = ["Cinematic Pan", "Dynamic Zoom", "Handheld POV", "Slow-motion"]
        for i, script in enumerate(scripts):
            mov = movements[i % len(movements)]
            negative = f"Shot {i+1:02d} Negative: low quality, blurry, distorted, glitch, color bleed, watermark, low resolution, messy textures, robotic voice, formal language, text overlap, no motion blur, no frame tearing, do not change logo position, do not alter fabric color"
            if "Pan" in mov:
                negative += ", no motion blur, no frame tearing, smooth transition"
            elif "Zoom" in mov:
                negative += ", no pixelation, no quality loss, sharp focus"
            elif "POV" in mov:
                negative += ", no excessive shake, no disorientation, stable"
            elif "Slow" in mov:
                negative += ", no frame skipping, no ghosting, fluid motion"
            negatives.append(negative)
        return negatives

    def generate_product_card(self, title, niche, features):
        return f"""[PRODUCT INFO CARD]
Product Name: {title}
Category: {niche.upper()}
Key Features: {features[:100]}"""

    def generate_video_brief_card(self, niche, duration, audience):
        shots = self.shot_counts[duration]
        return f"""[VIDEO BRIEF CARD]
Niche: {niche}
Duration: {duration} seconds
Shot Count: {shots} shots
Target Audience: {audience}
Mood: Energetic, Budol vibe, Professional"""

    def generate_analysis_card(self, duration, shots):
        return f"""[VIDEO ANALYSIS RESULTS]
Total Shots: {shots}
Audio Style: Taglish voiceover (clear, professional)
Lighting Guide: Natural/Studio/Neon
Resolution: 4K Vertical 9:16
Duration: {duration}s (3s per shot rule)
Infinity Loop: Enabled - video auto-replays seamlessly"""

    def generate_storyboard_card(self, scripts):
        storyboard = "[VIDEO STORYBOARD CARD]\n"
        for script in scripts[:5]:
            storyboard += script + "\n"
        storyboard += "... [continues for all shots]"
        return storyboard

    def save_to_supabase(self, input_data, analysis, final_output):
        try:
            import supabase
            from supabase import create_client
            import os
            url = os.environ.get("SUPABASE_URL")
            key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
            if url and key:
                client = create_client(url, key)
                data = {
                    "id": str(uuid.uuid4()),
                    "input_fields": input_data,
                    "analysis_output": analysis,
                    "final_output": final_output,
                    "created_at": datetime.now().isoformat()
                }
                client.table("chat_history").insert(data).execute()
                return True
        except:
            return False

    def generate(self, product_title, about_this_product, product_description, image_url):
        niche = self.detect_niche(product_title, about_this_product, product_description)
        duration = random.choice(self.durations)
        shots = self.shot_counts[duration]
        features = product_description[:100] if product_description else "Premium quality"
        audience = "Filipino TikTok users" if niche == "general" else f"Filipino {niche} enthusiasts"
        image_status = self.analyze_image_url(image_url)
        scripts = self.generate_positive_prompt(niche, duration, product_title, shots)
        positives = "\n".join(scripts)
        negatives = self.generate_negative_prompt(scripts)
        negatives_text = "\n".join(negatives)
        final_title = f"🔥 MUST-HAVE! {product_title[:40]} | {niche.upper()} Finds #TikTokMadeMeBuyIt #BudolFinds #Sulit #Quality #Affiliate"
        product_card = self.generate_product_card(product_title, niche, features)
        brief_card = self.generate_video_brief_card(niche, duration, audience)
        analysis_card = self.generate_analysis_card(duration, shots)
        storyboard_card = self.generate_storyboard_card(scripts)
        input_data = {
            "product_title": product_title,
            "about_this_product": about_this_product,
            "product_description": product_description,
            "image_url": image_url
        }
        analysis_output = {
            "niche": niche,
            "duration": duration,
            "shots": shots,
            "image_status": image_status
        }
        final_output = {
            "positive_prompt": positives,
            "negative_prompt": negatives_text,
            "final_title": final_title
        }
        self.save_to_supabase(input_data, analysis_output, final_output)
        output = f"""
============================================================
FINAL OUTPUT - COLUMN MAPPING
============================================================

{product_card}

{brief_card}

{analysis_card}

{storyboard_card}

============================================================

Column: positive_prompt

{positives}

============================================================

Column: negative_prompt

{negatives_text}

============================================================

Column: final_title

{final_title}

============================================================

MATCHING PROMPTS (Shot by Shot):
"""
        for i in range(min(len(scripts), len(negatives))):
            output += f"\nShot {i+1:02d}: positive_prompt = negative_prompt"
        
        output += f"""

============================================================
System Name: TikTok-Prompt-Generator-V1
DNA-Signature: HOOPSTREET-AFFILIATE-LOGIC-2026
Detected Niche: {niche}
Region: PH-LOCALIZED
Duration: {duration}s
Shots: {shots}
Image Status: {image_status}
Conversation ID: {self.conversation_id}
Infinity Loop: Enabled
============================================================
"""
        return output

generator = TikTokProductGenerator()

with gr.Blocks(title="TikTok-Prompt-Generator", theme="soft") as demo:
    gr.Markdown("# TikTok-Prompt-Generator")
    gr.Markdown("Generate TikTok affiliate content - Philippines Market")
    
    with gr.Row():
        with gr.Column(scale=1):
            product_title = gr.Textbox(label="Product Title", placeholder="Enter product name")
            about_this_product = gr.Textbox(label="About This Product", lines=2)
            product_description = gr.Textbox(label="Product Description", lines=3)
            image_url = gr.Textbox(label="Image URL", placeholder="https://...")
            submit = gr.Button("Generate", variant="primary")
        
        with gr.Column(scale=1):
            output = gr.Textbox(label="Generated Output", lines=40)
    
    submit.click(
        fn=generator.generate,
        inputs=[product_title, about_this_product, product_description, image_url],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
