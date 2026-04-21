#!/usr/bin/env python3
import os, json
from datetime import datetime

def generate_dashboard():
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI DevOps Dashboard</title>
    <style>
        body { font-family: sans-serif; background: #0a0a0a; color: #e0e0e0; padding: 20px; }
        .container { max-width: 1000px; margin: 0 auto; }
        h1 { color: #ff6600; }
        .card { background: #1a1a1a; border-radius: 12px; padding: 20px; margin: 15px 0; border-left: 4px solid #ff6600; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }
        .badge { background: #00ff0022; color: #00ff00; padding: 4px 10px; border-radius: 20px; font-size: 11px; border: 1px solid #00ff0044; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #333; }
        a { color: #ff6600; text-decoration: none; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AI DevOps Dashboard</h1>
        <p>System Update: <span id="time"></span></p>
        <div class="grid">
            <div class="card"><h3>📊 Status</h3><p>🟢 Operational</p><p>v4.1.0</p></div>
            <div id="api-card" class="card"><h3>🔑 API Keys</h3><p>Checking...</p></div>
        </div>
        <div class="card">
            <h3>🔍 Active AI Workflows</h3>
            <div class="grid" style="margin-top:10px;">
                <div>Analyzer <span class="badge">ACTIVE</span></div>
                <div>Auto-Fix <span class="badge">ACTIVE</span></div>
                <div>Merge-Gate <span class="badge">ACTIVE</span></div>
                <div>Self-Healing <span class="badge">ACTIVE</span></div>
            </div>
        </div>
        <div class="card"><h3>📋 Roadmap (DNA.md)</h3><div id="roadmap">Syncing...</div></div>
        <div style="text-align:center; margin-top:30px;">
            <a href="https://github.com/hoopstreet/TikTok-Prompt-Generator/actions">View GitHub Actions</a>
        </div>
    </div>
    <script>
        document.getElementById('time').innerText = new Date().toLocaleString();
        fetch('https://raw.githubusercontent.com/hoopstreet/TikTok-Prompt-Generator/main/DNA.md')
            .then(r => r.text()).then(text => {
                const versions = text.match(/### v[\d.]+/g) || [];
                let rows = versions.map(v => `<tr><td>${v.replace('### ','')}</td><td>🟢 Live</td></tr>`).join('');
                document.getElementById('roadmap').innerHTML = '<table>' + rows + '</table>';
            }).catch(() => { document.getElementById('roadmap').innerText = 'Offline'; });
    </script>
</body>
</html>
"""
    with open('dashboard.html', 'w') as f: f.write(html)
    print("✅ Dashboard generated.")

if __name__ == "__main__": generate_dashboard()
