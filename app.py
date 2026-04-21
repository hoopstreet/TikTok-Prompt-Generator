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
        "apparel": {"keywords": ["shirt","pants","hoodie","dress","fabric","shorts","athletic"], "focus": ["Oversized Fit","Presko","breathable","aesthetic"], "hashtag": "#ApparelFinds"},
        "audio": {"keywords": ["earbuds","headphones","speaker","bass","wireless"], "focus": ["Crystal Clear","Bass-heavy","Cyberpunk","noise cancel"], "hashtag": "#AudioGear"},
        "gaming": {"keywords": ["gaming","mouse","keyboard","rgb","controller"], "focus": ["No Lag","RGB Setup","Pro-Player","mechanical"], "hashtag": "#GamingSetup"},
        "tech": {"keywords": ["charger","powerbank","cable","adapter","usb"], "focus": ["PD fast charge","Compact","LED indicator"], "hashtag": "#TechLife"},
        "home": {"keywords": ["lamp","organizer","storage","kitchen","furniture"], "focus": ["Aesthetic","space saver","organization"], "hashtag": "#HomeOrganizer"},
        "beauty": {"keywords": ["skincare","makeup","cream","lotion","serum"], "focus": ["Real skin results","texture swatches"], "hashtag": "#SkincarePH"},
        "motor": {"keywords": ["car","motorcycle","helmet","tire","oil"], "focus": ["Pogi Points","Upgrade","Easy DIY","porma"], "hashtag": "#CarAccessories"},
        "sports": {"keywords": ["basketball","mesh","jersey","sports"], "focus": ["Full Sublimation","moisture wicking","custom IGN"], "hashtag": "#SportsGear"},
        "tools": {"keywords": ["heavy-duty","rechargeable","cordless","handy"], "focus": ["Heavy-duty","High torque","multi-bit"], "hashtag": "#ToolTime"},
        "pets": {"keywords": ["dog","cat","pet","chew","toy"], "focus": ["Durable","Chew-resistant","non-toxic"], "hashtag": "#PetLife"}
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
    def generate_positive_prompt(self, niche, shots, timings):
        n_data = self.NICHES.get(niche, self.NICHES["apparel"])
        scripts = []
        for i in range(shots):
            tag, act = self.TAGLISH_PHRASES[i % len(self.TAGLISH_PHRASES)]
            scripts.append(f"Shot {i+1:02d} ({timings[i]}s): 4K vertical [{self.CAMERAS[i%4]}] [{self.LIGHTING[i%4]}] [{self.FRAMING[i%4]}] Show {n_data['focus'][i%len(n_data['focus'])]}. {act}.\nDialogue: \"{tag}\"")
        return "\n\n".join(scripts)

    def generate_negative_prompt(self, shots):
        negs = []
        for i in range(shots):
            negs.append(f"Shot {i+1:02d} Negative: low quality, blurry, distorted, glitch, watermark, robotic voice, formal language")
        return "\n\n".join(negs)

    def generate_final_title(self, product_title, niche):
        n_data = self.NICHES.get(niche, self.NICHES["apparel"])
        hashtags = "#TikTokMadeMeBuyIt #BudolFinds #Sulit #Quality " + n_data["hashtag"]
        return f"🔥 MUST-HAVE! {product_title[:40]} | {niche.upper()} {hashtags}"[:100]

    def generate(self, title, about, desc, image_url=""):
        niche = self.detect_niche(title, about, desc)
        duration = random.choice(list(self.DURATIONS.keys()))
        shots = self.DURATIONS[duration]
        timings = self.generate_shot_timings(duration, shots)
        pos = self.generate_positive_prompt(niche, shots, timings)
        neg = self.generate_negative_prompt(shots)
        f_title = self.generate_final_title(title, niche)
        output = f"FINAL TITLE:\n{f_title}\n\nPOSITIVE PROMPT:\n{pos}\n\nNEGATIVE PROMPT:\n{neg}"
        entry = {"id": len(self.history)+1, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "product_title": title, "final_title": f_title, "positive_preview": pos[:150], "full_output": output}
        self.history.append(entry)
        return output, self.history
ai_core = AITrainingCore()
custom_css = "body, .gradio-container { background-color: #1b1b1f !important; } .gr-button-primary { background-color: #FF6600 !important; }"

def gen_and_up(t, a, d, i):
    out, hist = ai_core.generate(t, a, d, i)
    table = [[h["id"], h["timestamp"], h["product_title"], h["final_title"], h["positive_preview"]] for h in hist]
    return out, hist, table

with gr.Blocks(title="TikTok Prompt Generator v4.0", css=custom_css) as demo:
    gr.Markdown("# 🎬 TikTok Prompt Generator v4.0\n**Philippines Market Edition**")
    with gr.Row():
        with gr.Column():
            title_in = gr.Textbox(label="Product Title")
            about_in = gr.Textbox(label="About", lines=2)
            desc_in = gr.Textbox(label="Description", lines=4)
            img_in = gr.Textbox(label="Image URL (Optional)")
            gen_btn = gr.Button("🚀 Generate Prompt", variant="primary")
        with gr.Column():
            out_box = gr.Textbox(label="Output", lines=20)
    
    hist_table = gr.Dataframe(headers=["ID", "Time", "Product", "Title", "Preview"], label="History")
    h_state = gr.State([])

    gen_btn.click(gen_and_up, [title_in, about_in, desc_in, img_in], [out_box, h_state, hist_table])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
