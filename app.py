import gradio as gr
import random
import re
import requests
import json
import uuid
import pandas as pd
from datetime import datetime
from PIL import Image
from io import BytesIO, StringIO

class TikTokProductGenerator:
    def __init__(self):
        self.durations = [15, 30, 45, 55]
        self.shot_counts = {15: 5, 30: 10, 45: 15, 55: 18}
        self.history = []
        self.selected_rows = []
        self.conversation_id = str(uuid.uuid4())
        
    def detect_niche(self, title, about, description):
        text = (title + " " + about + " " + description).lower()
        niches = {
            "apparel": ["shirt", "pants", "hoodie", "dress", "fabric", "shorts", "athletic", "varsity"],
            "audio": ["earbuds", "headphones", "speaker", "bass", "wireless"],
            "gaming": ["gaming", "mouse", "keyboard", "rgb", "controller"],
            "tech": ["charger", "powerbank", "cable", "adapter", "usb"],
            "motor": ["car", "motorcycle", "helmet", "tire", "oil"],
            "home": ["lamp", "organizer", "storage", "kitchen", "furniture"],
            "beauty": ["skincare", "makeup", "cream", "lotions", "serum"],
            "sports": ["basketball", "mesh", "jersey", "sports"],
            "tools": ["heavy-duty", "rechargeable", "cordless", "handy"],
            "pets": ["dog", "cat", "pet", "chew", "toy"]
        }
        for niche, keywords in niches.items():
            if any(k in text for k in keywords):
                return niche
        return "general"

    def analyze_image_url(self, image_url):
        if not image_url:
            return "No image provided"
        try:
            if "ibyteimg.com" in image_url or "tos-alisg" in image_url:
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

    def analyze_product(self, title, about, description, image_url):
        niche = self.detect_niche(title, about, description)
        image_status = self.analyze_image_url(image_url)
        text = (title + " " + about + " " + description).lower()
        features = []
        if "stretchy" in text or "stretch" in text:
            features.append("Stretchy fabric")
        if "lightweight" in text:
            features.append("Lightweight material")
        if "pocket" in text:
            features.append("Side pockets")
        if "elastic" in text:
            features.append("Elastic waistband")
        if "breathable" in text:
            features.append("Breathable fabric")
        if not features:
            features = ["Premium quality", "Comfortable fit"]
        return {
            "niche": niche,
            "image_status": image_status,
            "detected_features": features,
            "product_text_analysis": text[:200]
        }

    def generate_positive_prompt(self, niche, duration, product_name, shots, product_features):
        scripts = []
        taglish_dialogues = [
            ("Grabe ang ganda nito! Sulit na sulit sa unang kita pa lang.", "Close-up product display"),
            ("Solid ang quality mga idol! Ang tela presko at komportable.", "Fabric texture and feel"),
            ("Sulit na sulit sa presyo! Quality na quality hindi ka magsisisi.", "Price and value reveal"),
            ("Kunin niyo na yung sa'yo! Bilis ubos na ang stock.", "Call to action with basket"),
            ("Kailangan niyo to sa araw-araw! Sobrang useful at praktikal.", "Daily use demonstration"),
            ("Swerte niyo mga idol! Limited edition ito kaya grab na.", "Excitement and urgency"),
            ("Panalo to mga boss! Best investment para sa inyo.", "Winner celebration"),
            ("Mura pero quality! Budget-friendly na hindi tinipid sa tela.", "Price comparison")
        ]
        movements = ["Cinematic Pan", "Dynamic Zoom-in", "Handheld POV shake", "Slow-motion reveal"]
        lighting = ["Soft Studio Lighting", "Natural Sunlight", "Neon Glow", "Warm Golden Hour"]
        for i in range(shots):
            taglish, action = taglish_dialogues[i % len(taglish_dialogues)]
            mov = movements[i % len(movements)]
            lit = lighting[i % len(lighting)]
            feature_text = product_features[i % len(product_features)] if product_features else "Product feature"
            script = f"""Shot {i+1:02d} ({duration/shots:.1f}s): 4K vertical 9:16
Camera: {mov}
Lighting: {lit}
Framing: Medium Shot then Close-up
Visual: Show {feature_text}. Logo visible.
Dialogue: "{taglish}"
Background: Clean, uncluttered."""
            scripts.append(script)
        return scripts

    def generate_negative_prompt(self, scripts):
        negatives = []
        movements = ["Cinematic Pan", "Dynamic Zoom-in", "Handheld POV shake", "Slow-motion reveal"]
        for i, script in enumerate(scripts):
            mov = movements[i % len(movements)]
            negative = f"""Shot {i+1:02d} Negative: low quality, blurry, distorted, glitch, color bleed, deformed, watermark, text overlay, low resolution, pixelation, messy textures, robotic voice, unnatural speech, formal language, Taglish required, text overlap, logo position change, fabric color alteration, object morphing, background clutter, poor lighting, lens flare, frame tearing."""
            if "Pan" in mov:
                negative += " no motion blur, no frame tearing, smooth transition."
            elif "Zoom" in mov:
                negative += " no pixelation, no quality loss, sharp focus."
            elif "POV" in mov:
                negative += " no excessive shake, no disorientation, stable."
            elif "Slow" in mov:
                negative += " no frame skipping, no ghosting, fluid motion."
            negatives.append(negative)
        return negatives

    def generate_final_title(self, product_title, about, description, niche):
        hashtags = " #TikTokMadeMeBuyIt #BudolFinds #Sulit #Quality #Affiliate"
        text_source = (product_title + " " + about + " " + description)[:60]
        base_title = f"🔥 MUST-HAVE! {text_source} | {niche.upper()}"
        final_title = base_title + hashtags
        if len(final_title) > 100:
            base_title = f"🔥 {text_source[:50]} | {niche.upper()}"
            final_title = base_title + hashtags
        if len(final_title) > 100:
            base_title = f"🔥 {product_title[:40]}"
            final_title = base_title + hashtags
        if len(final_title) < 80:
            extra = description[:30] if description else "Shop now"
            final_title = f"🔥 {product_title[:40]} - {extra}{hashtags}"
        return final_title[:100]

    def save_to_supabase(self, input_data, analyst_data, final_output):
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
                    "input_field": input_data,
                    "analyst_product": analyst_data,
                    "final_output": final_output,
                    "created_at": datetime.now().isoformat()
                }
                client.table("generation_history").insert(data).execute()
                return True
        except:
            return False
    def generate(self, product_title, about_this_product, product_description, image_url):
        analyst_data = self.analyze_product(product_title, about_this_product, product_description, image_url)
        niche = analyst_data["niche"]
        duration = random.choice(self.durations)
        shots = self.shot_counts[duration]
        features = analyst_data["detected_features"]
        
        scripts = self.generate_positive_prompt(niche, duration, product_title, shots, features)
        positives = "\n\n".join(scripts)
        negatives_list = self.generate_negative_prompt(scripts)
        negatives = "\n\n".join(negatives_list)
        final_title = self.generate_final_title(product_title, about_this_product, product_description, niche)
        
        output = f"""positive_prompt

{positives}

---

negative_prompt

{negatives}

---

final_title

{final_title}"""
        
        input_data = {
            "product_title": product_title,
            "about_this_product": about_this_product,
            "product_description": product_description,
            "image_url": image_url
        }
        final_output_data = {
            "positive_prompt": positives,
            "negative_prompt": negatives,
            "final_title": final_title
        }
        self.save_to_supabase(input_data, analyst_data, final_output_data)
        
        history_entry = {
            "id": len(self.history) + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "positive_prompt": positives[:300] + "...",
            "negative_prompt": negatives[:300] + "...",
            "final_title": final_title,
            "full_output": output
        }
        self.history.append(history_entry)
        
        return output, self.history
    def export_to_csv(self, selected_data):
        if not selected_data:
            return "No data selected"
        df = pd.DataFrame([{
            "ID": h["id"],
            "Timestamp": h["timestamp"],
            "Positive Prompt": h["positive_prompt"],
            "Negative Prompt": h["negative_prompt"],
            "Final Title": h["final_title"]
        } for h in selected_data])
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        return csv_buffer.getvalue()
    
    def export_to_json(self, selected_data):
        if not selected_data:
            return "No data selected"
        export_data = [{
            "id": h["id"],
            "timestamp": h["timestamp"],
            "positive_prompt": h["positive_prompt"],
            "negative_prompt": h["negative_prompt"],
            "final_title": h["final_title"]
        } for h in selected_data]
        return json.dumps(export_data, indent=2)
    
    def export_to_markdown(self, selected_data):
        if not selected_data:
            return "No data selected"
        md = "# Selected Generation History\n\n"
        md += "| ID | Timestamp | Positive Prompt | Negative Prompt | Final Title |\n"
        md += "|----|-----------|-----------------|-----------------|-------------|\n"
        for h in selected_data:
            pos_short = h["positive_prompt"][:50] + "..." if len(h["positive_prompt"]) > 50 else h["positive_prompt"]
            neg_short = h["negative_prompt"][:50] + "..." if len(h["negative_prompt"]) > 50 else h["negative_prompt"]
            md += f"| {h['id']} | {h['timestamp']} | {pos_short} | {neg_short} | {h['final_title']} |\n"
        return md
    
    def get_selected_data(self, history, selected_indices):
        if not selected_indices:
            return []
        return [history[i-1] for i in selected_indices if i-1 < len(history)]

generator = TikTokProductGenerator()

def toggle_select_all(select_all, history):
    if select_all:
        return list(range(1, len(history) + 1))
    return []

def export_with_format(history, selected_ids, format_type):
    selected_data = [h for h in history if h["id"] in selected_ids]
    if format_type == "CSV":
        return generator.export_to_csv(selected_data)
    elif format_type == "JSON":
        return generator.export_to_json(selected_data)
    elif format_type == "Markdown":
        return generator.export_to_markdown(selected_data)
    return "Select format"

custom_css = """
body, .gradio-container { background-color: #1b1b1f !important; }
.gr-button-primary { background-color: #FF6600 !important; border-color: #FF6600 !important; }
.gr-button-primary:hover { background-color: #FF5500 !important; }
input[type="checkbox"] { accent-color: #FF6600 !important; }
.gr-dataframe { background-color: #2a2a2e !important; color: #FFFFFF !important; }
footer { visibility: hidden; }
"""

with gr.Blocks(title="TikTok-Prompt-Generator") as demo:
    gr.Markdown("# 🎬 TikTok-Prompt-Generator")
    
    with gr.Row():
        with gr.Column(scale=1):
            product_title = gr.Textbox(label="Product Title", placeholder="Enter product name")
            about_this_product = gr.Textbox(label="About This Product", lines=2)
            product_description = gr.Textbox(label="Product Description", lines=3)
            image_url = gr.Textbox(label="Image URL", placeholder="https://...")
            generate_btn = gr.Button("Generate", variant="primary")
    
    with gr.Row():
        with gr.Column(scale=1):
            output = gr.Textbox(label="Generated Output", lines=20)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Generation History")
            with gr.Row():
                select_all_checkbox = gr.Checkbox(label="Select All", scale=0)
                format_dropdown = gr.Dropdown(label="Format", choices=["CSV", "JSON", "Markdown"], scale=1)
                export_btn = gr.Button("Download", scale=0, size="sm")
            
            history_display = gr.Dataframe(
                label="",
                headers=["ID", "Timestamp", "Positive Prompt", "Negative Prompt", "Final Title"],
                interactive=False,
                wrap=True
            )
    
    history_state = gr.State([])
    selected_ids_state = gr.State([])
    
    generate_btn.click(
        fn=generator.generate,
        inputs=[product_title, about_this_product, product_description, image_url],
        outputs=[output, history_state]
    ).then(
        fn=lambda h: [[h[i]["id"], h[i]["timestamp"], h[i]["positive_prompt"], h[i]["negative_prompt"], h[i]["final_title"]] for i in range(len(h))],
        inputs=[history_state],
        outputs=[history_display]
    )
    
    select_all_checkbox.change(
        fn=toggle_select_all,
        inputs=[select_all_checkbox, history_state],
        outputs=[selected_ids_state]
    )
    
    def get_selected_from_table(evt: gr.SelectData, history):
        if evt.index:
            return [history[i]["id"] for i in evt.index if i < len(history)]
        return []
    
    history_display.select(
        fn=get_selected_from_table,
        inputs=[history_state],
        outputs=[selected_ids_state]
    )
    
    export_btn.click(
        fn=export_with_format,
        inputs=[history_state, selected_ids_state, format_dropdown],
        outputs=[output]
    )

demo.launch(server_name="0.0.0.0", server_port=7860, css=custom_css)
