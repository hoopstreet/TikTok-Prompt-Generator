import gradio as gr
import random
import re

class TikTokAIGenerator:
    def __init__(self):
        self.durations = [15, 30, 45]
        self.shot_counts = {15: 5, 30: 10, 45: 15}

    def detect_niche(self, title, description):
        text = (title + " " + description).lower()
        niches = {
            "audio": ["earbuds", "headphones", "speaker", "bass", "wireless"],
            "apparel": ["shirt", "pants", "hoodie", "dress", "fabric"],
            "gaming": ["gaming", "mouse", "keyboard", "rgb", "controller"],
            "tech": ["charger", "powerbank", "cable", "adapter", "usb"],
            "motor": ["car", "motorcycle", "helmet", "tire", "oil"],
            "home": ["lamp", "organizer", "storage", "kitchen", "furniture"]
        }
        for niche, keywords in niches.items():
            if any(k in text for k in keywords):
                return niche
        return "general"

    def generate_taglish_script(self, niche, duration, product_name):
        shots = self.shot_counts[duration]
        scripts = []
        taglish_lines = [
            ("Grabe ang ganda nito!", "Amazing quality"),
            ("Solid ang quality mga idol!", "Great quality guys"),
            ("Sulit na sulit sa presyo!", "Very worth it"),
            ("Kunin niyo na yung sa'yo!", "Get yours now"),
            ("Kailangan niyo to!", "You need this"),
            ("Swerte niyo mga idol!", "You're lucky guys"),
            ("Panalo to mga boss!", "This is a winner"),
            ("Mura pero quality!", "Cheap but quality")
        ]

        for i in range(shots):
            taglish, english = taglish_lines[i % len(taglish_lines)]
            scripts.append(
                f"Shot {i+1:02d} (3s): [4K vertical 9:16] "
                f"[Product showcase] {taglish}"
            )
        return scripts
    def generate(self, title, description, product_details, image_url):
        niche = self.detect_niche(title, description)
        duration = random.choice(self.durations)
        shots = self.shot_counts[duration]

        scripts = self.generate_taglish_script(niche, duration, title)

        output = f"""
================================================================================
2. Final Output (Column Mapping)
================================================================================

Column: positive_prompt

"""
        for script in scripts:
            output += script + "\n"
        output += f"""
================================================================================

Column: negative_prompt

low quality, blurry, distorted, glitch, color bleed, watermark,
low resolution, messy textures, robotic voice, formal language,
text overlap, no motion blur, no frame tearing

================================================================================

Column: final_title

🔥 MUST-HAVE! {title[:50]} | {niche.upper()} Finds
#TikTokMadeMeBuyIt #BudolFinds #Sulit #Quality #Affiliate
================================================================================

System Name: TikTok-Prompt-Generator-V1
DNA-Signature: HOOPSTREET-AFFILIATE-LOGIC-2026
Detected Niche: {niche}
Region: PH-LOCALIZED
Duration: {duration}s
Shots: {shots}
Generation Timestamp: 2026-04-19

================================================================================
"""
        return output

generator = TikTokAIGenerator()
with gr.Blocks(title="TikTok Prompt Generator", theme="soft") as demo:
    gr.Markdown("# 🤖 TikTok Affiliate AI Generator")
    gr.Markdown("### Philippines Market - Moondream 3 Integration")

    with gr.Row():
        with gr.Column(scale=1):
            title = gr.Textbox(label="Product Title")
            description = gr.Textbox(label="Product Description", lines=3)
            product_details = gr.Textbox(label="Additional Details", lines=2)
            image_url = gr.Textbox(label="Image URL (optional)")
            submit = gr.Button("Generate TikTok Script")

        with gr.Column(scale=1):
            output = gr.Textbox(label="Generated Output", lines=25)

    submit.click(
        fn=generator.generate,
        inputs=[title, description, product_details, image_url],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
