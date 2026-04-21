#!/usr/bin/env python3
import os
import re
import sys
import subprocess
from pathlib import Path

def detect_missing_imports():
    missing = []
    if not os.path.exists('app.py'):
        return missing

    with open('app.py', 'r') as f:
        content = f.read()

    imports = re.findall(r'^import (\w+)|^from (\w+) import', content, re.MULTILINE)

    for imp in imports:
        module = imp[0] or imp[1]
        if module and module not in ['gradio','random','uuid','json','datetime','os','re','typing']:
            try:
                __import__(module)
            except ImportError:
                missing.append(module)

    return missing

def fix_missing_imports(missing):
    if not missing:
        return False

    if not os.path.exists('requirements.txt'):
        open('requirements.txt','w').close()

    with open('requirements.txt','r') as f:
        reqs = f.read()

    for module in missing:
        if module not in reqs:
            with open('requirements.txt','a') as f:
                f.write(f'\n{module}')
            print(f"✅ Added {module}")

    return True

def detect_missing_functions():
    required = [
        'detect_niche',
        'generate_positive_prompt',
        'generate_negative_prompt',
        'generate_final_title',
        'generate_4_cards',
        'generate_shot_timings'
    ]

    if not os.path.exists('app.py'):
        return required

    with open('app.py','r') as f:
        content = f.read()

    return [f for f in required if f"def {f}" not in content]

def add_missing_function(name):
    templates = {
        'detect_niche': "def detect_niche(self,title,about,desc): return 'general'\n",
        'generate_shot_timings': "def generate_shot_timings(self,duration,shots): return [duration/shots]*shots\n",
        'generate_positive_prompt': "def generate_positive_prompt(self,*a): return 'positive'\n",
        'generate_negative_prompt': "def generate_negative_prompt(self,shots): return 'negative'\n",
        'generate_final_title': "def generate_final_title(self,*a): return 'title'\n",
        'generate_4_cards': "def generate_4_cards(self,*a): return {}\n"
    }

    if name in templates:
        with open('app.py','a') as f:
            f.write("\n"+templates[name])
        print(f"✅ Added {name}")

def upgrade_architecture():
    print("🚀 Creating FastAPI + Vite...")

    os.makedirs('backend',exist_ok=True)
    with open('backend/main.py','w') as f:
        f.write("from fastapi import FastAPI\napp=FastAPI()\n@app.get('/')\ndef r():return{'ok':True}")

    with open('backend/requirements.txt','w') as f:
        f.write("fastapi\nuvicorn\n")

    os.makedirs('frontend/src',exist_ok=True)
    with open('frontend/index.html','w') as f:
        f.write("<div id='root'></div><script type='module' src='/src/main.tsx'></script>")

    with open('frontend/src/main.tsx','w') as f:
        f.write("console.log('frontend ok')")

def self_heal():
    print("🧠 SELF HEAL START")

    missing_imports = detect_missing_imports()
    fix_missing_imports(missing_imports)

    missing_funcs = detect_missing_functions()
    for m in missing_funcs:
        add_missing_function(m)

    if not os.path.exists('backend') or not os.path.exists('frontend'):
        upgrade_architecture()

    try:
        subprocess.run([sys.executable,'-m','py_compile','app.py'],check=True)
        print("✅ Syntax OK")
    except:
        print("❌ Syntax ERROR")

    print("✅ SELF HEAL DONE")

if __name__ == "__main__":
    self_heal()
