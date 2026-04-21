#!/usr/bin/env python3
"""
AI Fix Generator - Uses DeepSeek API to generate fixes
"""

import os
import json
import requests

def deepseek_generate(prompt):
    """Call DeepSeek API for code generation"""
    api_key = os.environ.get('DEEPSEEK_API_KEY')
    
    if not api_key:
        print("⚠️ No DeepSeek API key, using fallback")
        return fallback_fix(prompt)
    
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-coder",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a senior Python engineer. Generate fixes."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.2,
                "max_tokens": 1000
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"⚠️ API error: {e}")
    
    return fallback_fix(prompt)

def fallback_fix(prompt):
    """Rule-based fallback fixes"""
    return "# Auto-generated fix\n# Review before merging\n"

def main():
    # Load analysis report
    with open('analysis_report.json', 'r') as f:
        report = json.load(f)
    
    if report['total_issues'] == 0:
        print("✅ No issues found")
        return
    
    # Generate fix prompt
    prompt = f"""
    Fix these issues in the codebase:
    {json.dumps(report, indent=2)}
    
    Provide the fixed code for app.py.
    """
    
    fix = deepseek_generate(prompt)
    
    # Save fix for PR
    with open('fix_output.md', 'w') as f:
        f.write(fix)
    
    print("✅ Fix generated")

if __name__ == "__main__":
    main()
