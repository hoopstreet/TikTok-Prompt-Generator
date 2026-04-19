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
            if "ibyteimg.com" in image_url or "tos-alisg" in image_url:
                return "ByteDance CDN valid - TikTok Shop image"
            if "resize-webp" in image_url:
                return "WebP format optimized for mobile"
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
            script = f"""Shot {i+1:02d} ({duration/shots:.1f}s): 4K vertical 9:16 aspect ratio, high-detail resolution.
Camera Movement: {mov}
Lighting: {lit}
Shot Framing: Medium Shot (MS) for product context, then zoom to Close-up (CU) for details.
Visual Description: Show {feature_text}. Ensure product logo is visible and correctly positioned.
Dialogue (Taglish): "{taglish}"
Background: Clean, uncluttered background that does not distract from the product."""
            scripts.append(script)
        return scripts

    def generate_negative_prompt(self, scripts):
        negatives = []
        movements = ["Cinematic Pan", "Dynamic Zoom-in", "Handheld POV shake", "Slow-motion reveal"]
        for i, script in enumerate(scripts):
            mov = movements[i % len(movements)]
            negative = f"""Shot {i+1:02d} Negative: low quality, blurry, distorted, glitch, color bleed, deformed, watermark, text overlay, low resolution, pixelation, messy textures, robotic voice, unnatural speech, formal language, Taglish required not pure English, text overlap on product, logo position change, fabric color alteration, object morphing, inconsistent product appearance, background clutter, poor lighting, lens flare over product, excessive shadowing, frame tearing, stuttering playback."""
            if "Pan" in mov:
                negative += " no motion blur during pan, no frame tearing, smooth camera transition, consistent speed."
            elif "Zoom" in mov:
                negative += " no pixelation during zoom, no quality loss, sharp focus maintained, smooth zoom curve."
            elif "POV" in mov:
                negative += " no excessive camera shake, no disorientation, stable handheld movement, natural perspective."
            elif "Slow" in mov:
                negative += " no frame skipping during slow-mo, no ghosting artifacts, fluid motion, clear details."
            negatives.append(negative)
        return negatives

    def generate_final_title(self, product_title, niche):
        hashtags = " #TikTokMadeMeBuyIt #BudolFinds #Sulit #Quality #Affiliate"
        base_title = f"🔥 MUST-HAVE! {product_title[:40]} | {niche.upper()} Finds"
        final_title = base_title + hashtags
        if len(final_title) > 100:
            base_title = f"🔥 {product_title[:35]} | {niche.upper()}"
            final_title = base_title + hashtags
        if len(final_title) > 100:
            base_title = f"🔥 {product_title[:30]}"
            final_title = base_title + hashtags
        if len(final_title) < 80:
            final_title = f"🔥 MUST-HAVE! {product_title[:45]} | Shop now!{hashtags}"
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
        image_status = analyst_data["image_status"]
        
        scripts = self.generate_positive_prompt(niche, duration, product_title, shots, features)
        positives = "\n\n".join(scripts)
        negatives_list = self.generate_negative_prompt(scripts)
        negatives = "\n\n".join(negatives_list)
        final_title = self.generate_final_title(product_title, niche)
        
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
            "product_title": product_title[:50],
            "niche": niche,
            "output": output
        }
        self.history.append(history_entry)
        
        return output, self.history

    def export_to_csv(self, history):
        if not history:
            return "No history to export"
        df = pd.DataFrame(history)
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        return csv_buffer.getvalue()
    
    def export_to_json(self, history):
        if not history:
            return "No history to export"
        return json.dumps(history, indent=2)
    
    def export_to_markdown(self, history):
        if not history:
            return "No history to export"
        md = "# Generated Output History\n\n"
        for entry in history:
            md += f"## {entry['timestamp']} - {entry['product_title']}\n"
            md += f"**Niche:** {entry['niche']}\n\n"
            md += f"```\n{entry['output'][:500]}...\n```\n\n---\n\n"
        return md
    
    def clear_history(self):
        self.history = []
        return "History cleared", []

generator = TikTokProductGenerator()

def copy_output(output_text):
    return output_text

def export_selected_format(history, format_type):
    if format_type == "CSV":
        return generator.export_to_csv(history)
    elif format_type == "JSON":
        return generator.export_to_json(history)
    elif format_type == "Markdown":
        return generator.export_to_markdown(history)
    else:
        return "Invalid format"

with gr.Blocks(title="TikTok-Prompt-Generator", theme="soft") as demo:
    gr.Markdown("# TikTok-Prompt-Generator")
    
    with gr.Row():
        with gr.Column(scale=1):
            product_title = gr.Textbox(label="Product Title", placeholder="Enter product name")
            about_this_product = gr.Textbox(label="About This Product", lines=2)
            product_description = gr.Textbox(label="Product Description", lines=3)
            image_url = gr.Textbox(label="Image URL", placeholder="https://...")
            submit = gr.Button("Generate", variant="primary")
        
        with gr.Column(scale=1):
            output = gr.Textbox(label="Generated Output", lines=35)
            copy_btn = gr.Button("📋 Copy to Clipboard")
            copy_status = gr.Textbox(label="Copy Status", visible=False)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### History Management")
            refresh_btn = gr.Button("🔄 Refresh History")
            clear_btn = gr.Button("🗑️ Clear History")
            history_display = gr.Dataframe(label="Generation History", headers=["ID", "Timestamp", "Product", "Niche"])
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Export Options")
            format_dropdown = gr.Dropdown(label="Export Format", choices=["CSV", "JSON", "Markdown"])
            export_btn = gr.Button("📥 Export History")
            export_output = gr.Textbox(label="Export Data", lines=10)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Bulk Download")
            bulk_csv_btn = gr.Button("📊 Download CSV")
            bulk_json_btn = gr.Button("📄 Download JSON")
            bulk_md_btn = gr.Button("📝 Download Markdown")
            download_status = gr.Textbox(label="Download Status", visible=False)
    
    output_state = gr.State()
    history_state = gr.State([])
    
    submit.click(
        fn=generator.generate,
        inputs=[product_title, about_this_product, product_description, image_url],
        outputs=[output, history_state]
    ).then(
        fn=lambda h: [(i+1, h[i]['timestamp'], h[i]['product_title'], h[i]['niche']) for i in range(len(h))],
        inputs=[history_state],
        outputs=[history_display]
    )
    
    refresh_btn.click(
        fn=lambda h: [(i+1, h[i]['timestamp'], h[i]['product_title'], h[i]['niche']) for i in range(len(h))],
        inputs=[history_state],
        outputs=[history_display]
    )
    
    clear_btn.click(
        fn=generator.clear_history,
        inputs=[],
        outputs=[download_status, history_state]
    ).then(
        fn=lambda: [],
        inputs=[],
        outputs=[history_display]
    )
    
    copy_btn.click(
        fn=copy_output,
        inputs=[output],
        outputs=[copy_status]
    )
    
    export_btn.click(
        fn=export_selected_format,
        inputs=[history_state, format_dropdown],
        outputs=[export_output]
    )
    
    bulk_csv_btn.click(
        fn=lambda h: (generator.export_to_csv(h), "CSV exported"),
        inputs=[history_state],
        outputs=[export_output, download_status]
    )
    
    bulk_json_btn.click(
        fn=lambda h: (generator.export_to_json(h), "JSON exported"),
        inputs=[history_state],
        outputs=[export_output, download_status]
    )
    
    bulk_md_btn.click(
        fn=lambda h: (generator.export_to_markdown(h), "Markdown exported"),
        inputs=[history_state],
        outputs=[export_output, download_status]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
