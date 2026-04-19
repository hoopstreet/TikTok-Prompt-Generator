<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>DNA.md — Section 8: AI Developer Protocol</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #0a0e14;
    --surface: #0f1520;
    --panel: #131d2e;
    --border: #1e3050;
    --accent: #00d4ff;
    --accent2: #00ff88;
    --accent3: #ff6b35;
    --warn: #ffb800;
    --muted: #3a5070;
    --text: #c8ddf0;
    --text-dim: #6080a0;
    --rule-bg: #0d1a2a;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    min-height: 100vh;
    padding: 0;
    overflow-x: hidden;
  }

  /* Scanline overlay */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
      0deg,
      transparent,
      transparent 2px,
      rgba(0,212,255,0.015) 2px,
      rgba(0,212,255,0.015) 4px
    );
    pointer-events: none;
    z-index: 100;
  }

  .header {
    background: linear-gradient(135deg, #0a1520 0%, #0d1f35 100%);
    border-bottom: 1px solid var(--border);
    padding: 14px 16px 12px;
    position: sticky;
    top: 0;
    z-index: 50;
  }

  .header-path {
    font-size: 10px;
    color: var(--text-dim);
    letter-spacing: 0.08em;
    margin-bottom: 4px;
  }

  .header-path span {
    color: var(--accent);
  }

  .header-title {
    font-family: 'Space Mono', monospace;
    font-size: 15px;
    font-weight: 700;
    color: #fff;
    letter-spacing: -0.02em;
  }

  .header-title em {
    color: var(--accent2);
    font-style: normal;
  }

  .header-badges {
    display: flex;
    gap: 6px;
    margin-top: 8px;
    flex-wrap: wrap;
  }

  .badge {
    font-size: 9px;
    padding: 2px 7px;
    border-radius: 2px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }

  .badge-strict { background: #ff2a2a22; color: #ff5555; border: 1px solid #ff555540; }
  .badge-mobile { background: #00ff8822; color: var(--accent2); border: 1px solid #00ff8840; }
  .badge-ish    { background: #00d4ff22; color: var(--accent); border: 1px solid #00d4ff40; }
  .badge-auto   { background: #ffb80022; color: var(--warn); border: 1px solid #ffb80040; }

  .section-label {
    font-size: 9px;
    color: var(--text-dim);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 16px 16px 6px;
  }

  .rule-card {
    margin: 0 10px 10px;
    border-radius: 6px;
    border: 1px solid var(--border);
    background: var(--panel);
    overflow: hidden;
    transition: border-color 0.2s;
  }

  .rule-card:hover {
    border-color: var(--accent);
  }

  .rule-header {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    background: var(--rule-bg);
    border-bottom: 1px solid var(--border);
  }

  .rule-num {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    color: var(--text-dim);
    min-width: 24px;
  }

  .rule-keyword {
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    font-weight: 700;
    flex: 1;
  }

  .rule-icon {
    font-size: 15px;
    line-height: 1;
  }

  .rule-body {
    padding: 10px 12px;
  }

  /* Rule colors */
  .rule-dns   .rule-keyword { color: var(--accent); }
  .rule-no    .rule-keyword { color: #ff5555; }
  .rule-len   .rule-keyword { color: var(--warn); }
  .rule-eof   .rule-keyword { color: var(--accent2); }
  .rule-mob   .rule-keyword { color: #b388ff; }

  .rule-dns   { border-color: #00d4ff30; }
  .rule-no    { border-color: #ff555530; }
  .rule-len   { border-color: #ffb80030; }
  .rule-eof   { border-color: #00ff8830; }
  .rule-mob   { border-color: #b388ff30; }

  .code-block {
    background: #080e18;
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 10px 12px;
    font-size: 12px;
    line-height: 1.7;
    margin-bottom: 8px;
    position: relative;
    overflow-x: auto;
  }

  .code-block::before {
    content: attr(data-label);
    position: absolute;
    top: 4px;
    right: 8px;
    font-size: 9px;
    color: var(--text-dim);
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }

  .cmd { color: var(--accent2); }
  .path { color: var(--accent); }
  .str { color: #ffd080; }
  .kw { color: #ff79c6; }
  .comment { color: var(--muted); font-style: italic; }
  .num { color: var(--warn); }
  .err { color: #ff5555; }
  .ok { color: var(--accent2); }

  .rule-points {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .rule-points li {
    display: flex;
    gap: 8px;
    align-items: flex-start;
    font-size: 12px;
    color: var(--text);
    line-height: 1.5;
  }

  .rule-points li::before {
    content: '›';
    color: var(--text-dim);
    font-size: 14px;
    flex-shrink: 0;
    margin-top: -1px;
  }

  .invalid-tag {
    display: inline-block;
    background: #ff000020;
    color: #ff5555;
    border: 1px solid #ff555540;
    border-radius: 3px;
    font-size: 9px;
    padding: 1px 5px;
    font-weight: 700;
    letter-spacing: 0.05em;
    vertical-align: middle;
    margin-left: 4px;
  }

  .valid-tag {
    display: inline-block;
    background: #00ff8820;
    color: var(--accent2);
    border: 1px solid #00ff8840;
    border-radius: 3px;
    font-size: 9px;
    padding: 1px 5px;
    font-weight: 700;
    letter-spacing: 0.05em;
    vertical-align: middle;
    margin-left: 4px;
  }

  .divider-label {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 4px 10px 10px;
    font-size: 9px;
    color: var(--text-dim);
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }

  .divider-label::before,
  .divider-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
  }

  .copy-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    margin: 0 10px 6px auto;
    width: fit-content;
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text-dim);
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    padding: 4px 10px;
    border-radius: 3px;
    cursor: pointer;
    letter-spacing: 0.08em;
    transition: all 0.15s;
  }

  .copy-btn:hover {
    border-color: var(--accent);
    color: var(--accent);
  }

  .footer {
    margin: 20px 10px 30px;
    padding: 12px;
    border: 1px dashed var(--border);
    border-radius: 6px;
    text-align: center;
    font-size: 10px;
    color: var(--text-dim);
    line-height: 1.8;
    letter-spacing: 0.05em;
  }

  .footer span { color: var(--accent2); }

  /* Pulse animation on strict mode badge */
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }
  .badge-strict { animation: pulse 2s ease-in-out infinite; }

  /* Typing cursor */
  @keyframes blink { 50% { opacity: 0; } }
  .cursor::after {
    content: '█';
    color: var(--accent);
    animation: blink 1s step-start infinite;
    font-size: 11px;
    margin-left: 2px;
  }
</style>
</head>
<body>

<!-- HEADER -->
<div class="header">
  <div class="header-path">
    ~/DNA.md <span>§8</span> · iSH · iPhone
  </div>
  <div class="header-title">
    AI Developer Protocol <em>STRICT MODE</em>
  </div>
  <div class="header-badges">
    <span class="badge badge-strict">⚡ strict</span>
    <span class="badge badge-mobile">📱 mobile-first</span>
    <span class="badge badge-ish">iSH shell</span>
    <span class="badge badge-auto">🤖 auto-only</span>
  </div>
</div>

<div class="section-label">5 rules · enforced</div>

<!-- RULE 1: DNS FIRST -->
<div class="rule-card rule-dns">
  <div class="rule-header">
    <span class="rule-num">R1</span>
    <span class="rule-keyword">DNS FIRST</span>
    <span class="rule-icon">🌐</span>
  </div>
  <div class="rule-body">
    <div class="code-block" data-label="sh">
      <span class="cmd">echo</span> <span class="str">"nameserver 8.8.8.8"</span><br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">&gt;</span> <span class="path">/etc/resolv.conf</span>
    </div>
    <ul class="rule-points">
      <li>Run before any network operation</li>
      <li>Google DNS · hardcoded fallback</li>
    </ul>
  </div>
</div>

<!-- RULE 2: NO MANUAL EDITS -->
<div class="rule-card rule-no">
  <div class="rule-header">
    <span class="rule-num">R2</span>
    <span class="rule-keyword">NO MANUAL EDITS</span>
    <span class="rule-icon">🚫</span>
  </div>
  <div class="rule-body">
    <ul class="rule-points">
      <li><span class="err">Never</span> ask user to open <code>nano</code> / <code>vi</code></li>
      <li><span class="ok">Fully automated</span> script-based updates only</li>
      <li>All file writes via heredoc or sed/awk</li>
    </ul>
  </div>
</div>

<!-- RULE 3: HARD LENGTH LIMIT -->
<div class="rule-card rule-len">
  <div class="rule-header">
    <span class="rule-num">R3</span>
    <span class="rule-keyword">HARD LENGTH LIMIT</span>
    <span class="rule-icon">📏</span>
  </div>
  <div class="rule-body">
    <div class="code-block" data-label="rule">
      <span class="comment"># Line length enforcement</span><br>
      MAX_CHARS=<span class="num">150</span><br><br>
      <span class="comment"># Blocks &gt;150 chars WITHOUT split</span><br>
      <span class="err">→ INVALID ✗</span><br><br>
      <span class="comment"># MUST use multiple cat EOF parts</span><br>
      <span class="ok">→ SPLIT ✓</span>
    </div>
    <ul class="rule-points">
      <li>iSH terminal wraps at ~150 chars</li>
      <li>Long blocks = broken heredocs on mobile</li>
    </ul>
  </div>
</div>

<!-- RULE 4: EOF SAFETY -->
<div class="rule-card rule-eof">
  <div class="rule-header">
    <span class="rule-num">R4</span>
    <span class="rule-keyword">EOF SAFETY</span>
    <span class="rule-icon">📄</span>
  </div>
  <div class="rule-body">
    <div class="divider-label">correct pattern</div>
    <div class="code-block" data-label="heredoc">
      <span class="comment"># Start</span><br>
      <span class="cmd">cat</span> &lt;&lt; <span class="str">'EOF'</span> <span class="kw">&gt;</span> <span class="path">file</span><br>
      &nbsp;&nbsp;<span class="comment">... content ...</span><br>
      <span class="str">EOF</span>
    </div>
    <div class="divider-label">forbidden</div>
    <div class="code-block" data-label="bad">
      <span class="cmd">cat</span> &lt;&lt; <span class="str">'EOF'</span><br>
      &nbsp;&nbsp;<span class="err">cat &lt;&lt; 'EOF2'</span> <span class="invalid-tag">INVALID</span><br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span class="comment">never nest cat inside cat</span><br>
      <span class="err">EOF2</span><br>
      <span class="str">EOF</span>
    </div>
  </div>
</div>

<!-- RULE 5: MOBILE FIRST -->
<div class="rule-card rule-mob">
  <div class="rule-header">
    <span class="rule-num">R5</span>
    <span class="rule-keyword">MOBILE-FIRST</span>
    <span class="rule-icon">📱</span>
  </div>
  <div class="rule-body">
    <ul class="rule-points">
      <li>Assume <strong>iPhone iSH</strong> environment</li>
      <li>Break long strings into multi-line</li>
      <li>No commands requiring wide terminal</li>
      <li>Test paste-ability in iSH before shipping</li>
    </ul>
    <div class="code-block" data-label="example">
      <span class="comment"># ✗ too long for mobile</span><br>
      <span class="err">echo "This is a very long string that will wrap and break on iSH terminal"</span><br><br>
      <span class="comment"># ✓ split for mobile</span><br>
      <span class="ok">MSG="This is a very long"</span><br>
      <span class="ok">MSG="$MSG string split"</span><br>
      <span class="cmd">echo</span> <span class="str">"$MSG"</span>
    </div>
  </div>
</div>

<!-- COPY FULL SECTION BUTTON -->
<button class="copy-btn" onclick="copySection()">
  ⎘ copy DNA.md §8
</button>

<div class="footer">
  <span>DNA.md</span> · Section 8 of N · MKey Manager<br>
  Remote-replace via iSH · auto-deploy only<br>
  <span class="cursor">_</span>
</div>

<script>
function copySection() {
  const md = `## 8. AI Developer Protocol (STRICT MODE)

### Rule 1: DNS FIRST
\`\`\`sh
echo "nameserver 8.8.8.8" > /etc/resolv.conf
\`\`\`

### Rule 2: NO MANUAL EDITS
- Never ask user to open nano/vi
- Fully automated script-based updates only

### Rule 3: HARD LENGTH LIMIT
- Blocks >150 chars WITHOUT split = INVALID
- MUST split into multiple cat EOF parts

### Rule 4: EOF SAFETY
\`\`\`sh
# Start
cat << 'EOF' > file
EOF
# Never nest cat inside cat
\`\`\`

### Rule 5: MOBILE-FIRST
- Assume iPhone iSH environment
- Break long strings into multiple lines`;

  navigator.clipboard.writeText(md).then(() => {
    const btn = document.querySelector('.copy-btn');
    btn.textContent = '✓ copied!';
    btn.style.color = 'var(--accent2)';
    btn.style.borderColor = 'var(--accent2)';
    setTimeout(() => {
      btn.textContent = '⎘ copy DNA.md §8';
      btn.style.color = '';
      btn.style.borderColor = '';
    }, 2000);
  });
}
</script>
</body>
</html>
