import gradio as gr
import random
import uuid
import json
from datetime import datetime
import os

class AITrainingCore:
    SHOT_TIMINGS = [2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9,
                    3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8,
                    3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7,
                    4.8, 4.9, 5.0]
    
    DURATIONS = {
        15: 5, 18: 6, 20: 7, 22: 7, 25: 8, 28: 9, 30: 10,
        32: 11, 35: 12, 38: 13, 40: 13, 42: 14, 45: 15,
        48: 16, 50: 17, 55: 18
    }
    
    NICHES = {
        "apparel": {"keywords": ["shirt","pants","hoodie","dress","fabric","shorts","athletic"],
                    "focus": ["Oversized Fit","Presko","breathable","aesthetic"],
                    "hashtag": "#ApparelFinds"},
        "audio": {"keywords": ["earbuds","headphones","speaker","bass","wireless"],
                  "focus": ["Crystal Clear","Bass-heavy","Cyberpunk","noise cancel"],
                  "hashtag": "#AudioGear"},
        "gaming": {"keywords": ["gaming","mouse","keyboard","rgb","controller"],
                   "focus": ["No Lag","RGB Setup","Pro-Player","mechanical"],
                   "hashtag": "#GamingSetup"},
        "tech": {"keywords": ["charger","powerbank","cable","adapter","usb"],
                 "focus": ["PD fast charge","Compact","LED indicator"],
                 "hashtag": "#TechLife"},
        "home": {"keywords": ["lamp","organizer","storage","kitchen","furniture"],
                 "focus": ["Aesthetic","space saver","organization"],
                 "hashtag": "#HomeOrganizer"},
        "beauty": {"keywords": ["skincare","makeup","cream","lotion","serum"],
                   "focus": ["Real skin results","texture swatches"],
                   "hashtag": "#SkincarePH"},
        "motor": {"keywords": ["car","motorcycle","helmet","tire","oil"],
                  "focus": ["Pogi Points","Upgrade","Easy DIY","porma"],
                  "hashtag": "#CarAccessories"},
        "sports": {"keywords": ["basketball","mesh","jersey","sports"],
                   "focus": ["Full Sublimation","moisture wicking","custom IGN"],
                   "hashtag": "#SportsGear"},
        "tools": {"keywords": ["heavy-duty","rechargeable","cordless","handy"],
                  "focus": ["Heavy-duty","High torque","multi-bit"],
                  "hashtag": "#ToolTime"},
        "pets": {"keywords": ["dog","cat","pet","chew","toy"],
                 "focus": ["Durable","Chew-resistant","non-toxic"],
                 "hashtag": "#PetLife"}
    }
    TAGLISH_PHRASES = [
        ("Grabe ang ganda nito! Sulit na sulit!", "Close-up product display"),
        ("Solid ang quality mga idol! Presko at komportable.", "Fabric texture"),
        ("Sulit na sulit sa presyo! Quality na quality.", "Price value"),
        ("Kunin niyo na yung sa'yo! Bilis ubos na ang stock.", "CTA urgency"),
        ("Kailangan niyo to sa araw-araw! Sobrang useful.", "Daily use"),
        ("Swerte niyo mga idol! Limited edition kaya grab na.", "Excitement"),
        ("Panalo to mga boss! Best investment para sa inyo.", "Winner"),
        ("Mura pero quality! Budget-friendly na hindi tinipid.", "Price compare"),
        ("Grabe ang tela sobrang breathable at presko!", "Fabric breathability"),
        ("Aesthetic na aesthetic, bagay sa lahat ng outfit!", "Style aesthetics")
    ]
    
    CAMERAS = ["Cinematic Pan", "Dynamic Zoom-in", "Handheld POV", "Slow-motion"]
    LIGHTING = ["Soft Studio", "Natural Sunlight", "Neon Glow", "Golden Hour"]
    FRAMING = ["Close-up CU", "Medium Shot MS", "Macro Shot", "Wide Shot WS"]
    
    def __init__(self):
        self.history = []
        self.conversation_id = str(uuid.uuid4())
    
    def detect_niche(self, title, about, desc):
        text = (title + " " + about + " " + desc).lower()
        for niche, data in self.NICHES.items():
            if any(keyword in text for keyword in data["keywords"]):
                return niche
        return "general"
    def generate_shot_timings(self, duration, shots):
        timings = []
        remaining = duration
        for i in range(shots - 1):
            available = [t for t in self.SHOT_TIMINGS if t <= remaining - 2.1]
            t = random.choice(available if available else self.SHOT_TIMINGS)
            timings.append(t)
            remaining -= t
        timings.append(round(remaining, 1))
        return timings
    
    def generate_positive_prompt(self, niche, duration, product_name, shots, timings):
        niche_data = self.NICHES.get(niche, self.NICHES["apparel"])
        scripts = []
        for i in range(shots):
            taglish, action = self.TAGLISH_PHRASES[i % len(self.TAGLISH_PHRASES)]
            script = f"""Shot {i+1:02d} ({timings[i]}s): 4K vertical 9:16 aspect ratio, high-detail [{self.CAMERAS[i%4]}] [{self.LIGHTING[i%4]}] [{self.FRAMING[i%4]}] Show {niche_data["focus"][i%len(niche_data["focus"])]}. {action}.
Dialogue (Taglish): "{taglish}\""""
            scripts.append(script)
        return "\n\n".join(scripts)
    
    def generate_negative_prompt(self, shots):
        negatives = []
        anti_map = {"Cinematic Pan": "no motion blur", "Dynamic Zoom-in": "no pixelation", "Handheld POV": "stable", "Slow-motion": "fluid"}
        for i in range(shots):
            cam = self.CAMERAS[i % 4]
            neg = f"Shot {i+1:02d} Negative: low quality, blurry, distorted, glitch, watermark, {anti_map.get(cam, '')}"
            negatives.append(neg)
        return "\n\n".join(negatives)
    def generate_final_title(self, product_title, niche):
        niche_data = self.NICHES.get(niche, self.NICHES["apparel"])
        hashtags = ["#TikTokMadeMeBuyIt", "#BudolFinds", "#Sulit", "#Quality", niche_data["hashtag"]]
        base = f"🔥 MUST-HAVE! {product_title[:40]} | {niche.upper()} Finds"
        final_title = f"{base} {' '.join(hashtags)}"
        return final_title[:100]
    
    def generate_4_cards(self, product_name, niche, duration, shots, timings):
        niche_data = self.NICHES.get(niche, self.NICHES["apparel"])
        return {
            "card1_product_info": {"product_name": product_name, "category": niche.upper()},
            "card2_video_brief": {"duration": duration, "shot_count": shots, "shot_timing": timings},
            "card3_analysis": {"resolution": "4K Vertical 9:16", "audio": "Taglish VO"},
            "card4_storyboard": {"shots": [{"shot": i+1, "move": self.CAMERAS[i%4], "text": self.TAGLISH_PHRASES[i%len(self.TAGLISH_PHRASES)][0]} for i in range(shots)]}
        }
    def generate(self, product_title, about, desc, image_url=""):
        niche = self.detect_niche(product_title, about, desc)
        duration = random.choice(list(self.DURATIONS.keys()))
        shots = self.DURATIONS[duration]
        timings = self.generate_shot_timings(duration, shots)
        
        pos = self.generate_positive_prompt(niche, duration, product_title, shots, timings)
        neg = self.generate_negative_prompt(shots)
        title = self.generate_final_title(product_title, niche)
        cards = self.generate_4_cards(product_title, niche, duration, shots, timings)
        
        output = f"COLUMN: positive_prompt\n\n{pos}\n\nCOLUMN: negative_prompt\n\n{neg}\n\nCOLUMN: final_title\n\n{title}\n\nCARDS:\n{json.dumps(cards, indent=2)}"
        entry = {"id": len(self.history)+1, "timestamp": datetime.now().strftime("%H:%M:%S"), "product_title": product_title, "final_title": title, "positive_preview": pos[:100], "full_output": output}
        self.history.append(entry)
        return output, self.history

ai_core = AITrainingCore()

def update_table(history):
    return [[h["id"], h["timestamp"], h["product_title"], h["final_title"], h["positive_preview"]] for h in history]

def generate_and_update(t, a, d, i):
    o, h = ai_core.generate(t, a, d, i)
    return o, h, update_table(h)

def delete_history():
    ai_core.history = []
    return [], []
custom_css = "body, .gradio-container { background-color: #1b1b1f !important; color: white !important; }"

with gr.Blocks(title="TikTok Prompt Generator v4.0", css=custom_css) as demo:
    gr.Markdown("# 🎬 TikTok Prompt Generator v4.0\n**Philippines Market Edition**")
    with gr.Row():
        with gr.Column(scale=1):
            t = gr.Textbox(label="Product Title")
            a = gr.Textbox(label="About Product", lines=2)
            d = gr.Textbox(label="Description", lines=4)
            i = gr.Textbox(label="Image URL (Optional)")
            gen_btn = gr.Button("🚀 Generate Prompt", variant="primary")
            clear_btn = gr.Button("🗑️ Clear History")
        with gr.Column(scale=2):
            out = gr.Textbox(label="Generated Output", lines=20)
    
    history_table = gr.Dataframe(headers=["ID", "Time", "Product", "Title", "Preview"], label="History")
    h_state = gr.State([])

    gen_btn.click(generate_and_update, [t, a, d, i], [out, h_state, history_table])
    clear_btn.click(delete_history, None, [h_state, history_table])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
