import gradio as gr
import random
import json
import uuid
import pandas as pd
from datetime import datetime
from io import StringIO

class TikTokProductGenerator:
    def __init__(self):
        self.history = []
        self.selected_ids = []

    def generate_positive_prompt(self, title, niche):
        taglish_lines = [
            "Grabe ang ganda nito! Sulit na sulit sa unang kita pa lang.",
            "Solid ang quality mga idol! Ang tela presko at komportable.",
            "Sulit na sulit sa presyo! Quality na quality hindi ka magsisisi.",
            "Kunin niyo na yung sa'yo! Bilis ubos na ang stock.",
            "Kailangan niyo to sa araw-araw! Sobrang useful at praktikal."
        ]
        movements = ["Cinematic Pan", "Dynamic Zoom-in", "Handheld POV shake", "Slow-motion reveal"]
        lighting = ["Soft Studio Lighting", "Natural Sunlight", "Neon Glow"]
        shots = []
        for i in range(5):
            taglish = taglish_lines[i % len(taglish_lines)]
            mov = movements[i % len(movements)]
            lit = lighting[i % len(lighting)]
            shot = f"Shot {i+1:02d} (3.0s): 4K vertical 9:16 [{mov}] [{lit}] {taglish}"
            shots.append(shot)
        return "\n\n".join(shots)
    
    def generate_negative_prompt(self, shots_count=5):
        negatives = []
        for i in range(shots_count):
            neg = f"Shot {i+1:02d} Negative: low quality, blurry, distorted, glitch, color bleed, deformed, watermark, low resolution, messy textures, robotic voice, formal language, text overlap, do not change logo position, do not alter fabric color"
            negatives.append(neg)
        return "\n\n".join(negatives)
    
    def generate_final_title(self, title, niche):
        hashtags = " #TikTokMadeMeBuyIt #BudolFinds #Sulit #Quality #Affiliate"
        base = f"🔥 MUST-HAVE! {title[:40]} | {niche.upper()} Finds"
        final = base + hashtags
        if len(final) > 100:
            final = f"🔥 {title[:35]} | {niche.upper()}{hashtags}"
        if len(final) > 100:
            final = f"🔥 {title[:30]}{hashtags}"
        return final[:100]

    def generate(self, title, about, desc, img):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_id = len(self.history) + 1
        
        # Detect niche
        text = (title + " " + about + " " + desc).lower()
        niches = {"apparel": ["shirt", "pants", "hoodie", "dress", "fabric", "shorts"], "audio": ["earbuds", "headphones", "speaker"], "gaming": ["gaming", "mouse", "keyboard"], "tech": ["charger", "powerbank", "cable"]}
        niche = "general"
        for n, keywords in niches.items():
            if any(k in text for k in keywords):
                niche = n
                break
        
        pos = self.generate_positive_prompt(title, niche)
        neg = self.generate_negative_prompt(5)
        final_t = self.generate_final_title(title, niche)
        
        full_out = f"positive_prompt\n\n{pos}\n\n---\n\nnegative_prompt\n\n{neg}\n\n---\n\nfinal_title\n\n{final_t}"
        
        entry = {
            "id": new_id,
            "timestamp": timestamp,
            "positive_prompt": pos[:200] + "..." if len(pos) > 200 else pos,
            "negative_prompt": neg[:200] + "..." if len(neg) > 200 else neg,
            "final_title": final_t,
            "full_output": full_out
        }
        self.history.append(entry)
        return full_out, self.history

gen = TikTokProductGenerator()

custom_css = """
body, .gradio-container { background-color: #1b1b1f !important; }
.gr-button-primary { background-color: #FF6600 !important; border-color: #FF6600 !important; }
.gr-button-primary:hover { background-color: #FF5500 !important; }
/* Hide default copy button on textbox */
.gr-textbox button.gr-button { display: none !important; }
/* Table styling */
.history-table { width: 100%; border-collapse: collapse; background: #2a2a2e; color: #e0e0e0; border-radius: 8px; font-family: monospace; font-size: 13px; }
.history-table th { background: #1f1f23; color: #FF6600; padding: 12px 8px; border-bottom: 2px solid #FF6600; text-align: left; }
.history-table td { padding: 10px 8px; border-bottom: 1px solid #3a3a3e; vertical-align: middle; }
.history-table tr:hover { background-color: #3a3a3e; }
/* Checkbox alignment */
.history-table th:first-child, .history-table td:first-child { text-align: center; width: 40px; }
.history-table th:nth-child(2), .history-table td:nth-child(2) { width: 60px; }
.history-table th:nth-child(3), .history-table td:nth-child(3) { width: 160px; }
.history-table th:last-child, .history-table td:last-child { width: 50px; text-align: center; }
input[type="checkbox"] { accent-color: #FF6600; width: 18px; height: 18px; cursor: pointer; margin: 0; }
/* Cell copy icons */
.cell-copy { cursor: pointer; color: #FF6600; margin-left: 8px; font-size: 12px; opacity: 0.7; display: inline-block; background: transparent; border: none; }
.cell-copy:hover { opacity: 1; color: #FF8844; }
/* Download icon */
.download-icon { cursor: pointer; color: #FF6600; font-size: 18px; background: transparent; border: none; }
.download-icon:hover { color: #FF8844; }
/* Dropdown menu */
.dropdown-content { display: none; position: absolute; background: #2a2a2e; border: 1px solid #FF6600; min-width: 100px; border-radius: 4px; z-index: 1000; box-shadow: 0 2px 8px rgba(0,0,0,0.3); }
.dropdown-content a { color: white; padding: 8px 12px; text-decoration: none; display: block; cursor: pointer; font-size: 14px; }
.dropdown-content a:hover { background: #FF6600; color: #1b1b1f; }
.show { display: block; }
footer { visibility: hidden; }
"""

def get_table_html(history, selected_ids):
    if not history:
        return '<div style="padding: 40px; text-align: center; color: #888;">No history yet. Generate some prompts!</div>'
    
    html = '''
    <table class="history-table">
        <thead>
            <tr>
                <th><input type="checkbox" id="master_check" onchange="toggleAll(this)"></th>
                <th>ID</th>
                <th>Timestamp</th>
                <th>Positive Prompt</th>
                <th>Negative Prompt</th>
                <th>Final Title</th>
                <th><span class="download-icon" onclick="showBulkDrop(event)">⬇️</span></th>
            </tr>
        </thead>
        <tbody>
    '''
    
    for h in history:
        checked = 'checked' if h['id'] in selected_ids else ''
        pos_short = h['positive_prompt'][:80] + '...' if len(h['positive_prompt']) > 80 else h['positive_prompt']
        neg_short = h['negative_prompt'][:80] + '...' if len(h['negative_prompt']) > 80 else h['negative_prompt']
        title_short = h['final_title'][:80] + '...' if len(h['final_title']) > 80 else h['final_title']
        
        html += f'''
            <tr>
                <td style="text-align:center;"><input type="checkbox" class="row-check" data-id="{h['id']}" {checked} onchange="updateSelection()"></td>
                <td>{h['id']}<button class="cell-copy" onclick="copyText('{h['id']}')">📋</button></td>
                <td>{h['timestamp']}<button class="cell-copy" onclick="copyText('{h['timestamp']}')">📋</button></td>
                <td>{pos_short}<button class="cell-copy" onclick="copyText(`{h['positive_prompt']}`)">📋</button></td>
                <td>{neg_short}<button class="cell-copy" onclick="copyText(`{h['negative_prompt']}`)">📋</button></td>
                <td>{title_short}<button class="cell-copy" onclick="copyText('{h['final_title']}')">📋</button></td>
                <td style="text-align:center;"><button class="download-icon" onclick="showRowDrop(event, {h['id']})">⬇️</button></td>
            </tr>
        '''
    
    html += '''
        </tbody>
    </table>
    <div id="bulkDrop" class="dropdown-content"><a onclick="doExport('bulk', 'CSV')">CSV</a><a onclick="doExport('bulk', 'JSON')">JSON</a><a onclick="doExport('bulk', 'Markdown')">Markdown</a></div>
    <div id="rowDrop" class="dropdown-content"><a onclick="doExport('row', 'CSV')">CSV</a><a onclick="doExport('row', 'JSON')">JSON</a><a onclick="doExport('row', 'Markdown')">Markdown</a></div>
    <script>
        function copyText(text) { navigator.clipboard.writeText(text); }
        function toggleAll(source) { document.querySelectorAll('.row-check').forEach(cb => cb.checked = source.checked); updateSelection(); }
        function updateSelection() { let ids = Array.from(document.querySelectorAll('.row-check:checked')).map(cb => parseInt(cb.dataset.id)); let inp = document.querySelector('#selected_ids_input'); if(inp) { inp.value = JSON.stringify(ids); inp.dispatchEvent(new Event('change')); } }
        function showBulkDrop(e) { e.stopPropagation(); let menu = document.getElementById('bulkDrop'); menu.classList.toggle('show'); let rect = e.target.getBoundingClientRect(); menu.style.top = (rect.bottom + window.scrollY) + 'px'; menu.style.left = (rect.left + window.scrollX - 80) + 'px'; }
        function showRowDrop(e, rowId) { e.stopPropagation(); let menu = document.getElementById('rowDrop'); menu.classList.toggle('show'); menu.dataset.rowId = rowId; let rect = e.target.getBoundingClientRect(); menu.style.top = (rect.bottom + window.scrollY) + 'px'; menu.style.left = (rect.left + window.scrollX - 80) + 'px'; }
        function doExport(type, format) { let ids = []; if(type === 'bulk') { ids = Array.from(document.querySelectorAll('.row-check:checked')).map(cb => parseInt(cb.dataset.id)); } else { ids = [parseInt(document.getElementById('rowDrop').dataset.rowId)]; } let trigger = document.querySelector('#export_trigger'); if(trigger) { trigger.value = JSON.stringify({ids: ids, format: format}); trigger.dispatchEvent(new Event('input', {bubbles: true})); } document.getElementById('bulkDrop').classList.remove('show'); document.getElementById('rowDrop').classList.remove('show'); }
        document.addEventListener('click', function() { document.getElementById('bulkDrop').classList.remove('show'); document.getElementById('rowDrop').classList.remove('show'); });
        window.copyText = copyText; window.toggleAll = toggleAll; window.updateSelection = updateSelection; window.showBulkDrop = showBulkDrop; window.showRowDrop = showRowDrop; window.doExport = doExport;
    </script>
    '''
    return html

with gr.Blocks(title="TikTok-Prompt-Generator", css=custom_css, theme="dark") as demo:
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
            output = gr.Textbox(label="Generated Output", lines=20, show_copy_button=False)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Generation History")
            history_display = gr.HTML()
    
    history_state = gr.State([])
    selected_ids_input = gr.Textbox(visible=False, elem_id="selected_ids_input")
    export_trigger = gr.Textbox(visible=False, elem_id="export_trigger")
    download_file = gr.File(label="Download", visible=False)
    
    generate_btn.click(
        fn=gen.generate,
        inputs=[product_title, about_this_product, product_description, image_url],
        outputs=[output, history_state]
    ).then(
        fn=get_table_html,
        inputs=[history_state, gr.State([])],
        outputs=[history_display]
    )
    
    selected_ids_input.change(
        fn=lambda x: json.loads(x) if x else [],
        inputs=[selected_ids_input],
        outputs=[gr.State([])]
    ).then(
        fn=get_table_html,
        inputs=[history_state, gr.State([])],
        outputs=[history_display]
    )
    
    def do_export(export_data, history):
        if not export_data:
            return None
        data = json.loads(export_data)
        ids = data.get("ids", [])
        fmt = data.get("format", "CSV")
        selected = [h for h in history if h["id"] in ids]
        if not selected:
            return None
        df = pd.DataFrame([{
            "ID": h["id"],
            "Timestamp": h["timestamp"],
            "Positive Prompt": h["positive_prompt"],
            "Negative Prompt": h["negative_prompt"],
            "Final Title": h["final_title"]
        } for h in selected])
        ext = "csv" if fmt == "CSV" else "json" if fmt == "JSON" else "md"
        content = df.to_csv(index=False) if fmt == "CSV" else df.to_json(orient="records") if fmt == "JSON" else df.to_markdown(index=False)
        filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
        return gr.File(value=(content, filename), visible=True)
    
    export_trigger.change(do_export, [export_trigger, history_state], [download_file])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
