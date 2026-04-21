#!/usr/bin/env python3
import os, json, requests
from datetime import datetime

class MultiModelAI:
    def __init__(self):
        self.deepseek_key = os.environ.get("DEEPSEEK_API_KEY")
        self.hf_token = os.environ.get("HF_TOKEN")
        self.models = {
            "primary": {"name": "deepseek-coder", "type": "api", "endpoint": "https://api.deepseek.com/v1/chat/completions", "available": bool(self.deepseek_key)},
            "fallback_1": {"name": "CodeLlama-7b-hf", "type": "huggingface", "endpoint": "https://api-inference.huggingface.co/models/codellama/CodeLlama-7b-hf", "available": bool(self.hf_token)},
            "fallback_2": {"name": "starcoder2-3b", "type": "huggingface", "endpoint": "https://api-inference.huggingface.co/models/bigcode/starcoder2-3b", "available": bool(self.hf_token)}
        }
        self.active_model = self.select_best_model()
    
    def select_best_model(self):
        for key, model in self.models.items():
            if model["available"]: return model
        return None
    
    def call_deepseek(self, prompt):
        headers = {"Authorization": f"Bearer {self.deepseek_key}", "Content-Type": "application/json"}
        data = {"model": "deepseek-coder", "messages": [{"role": "system", "content": "You are a senior Python engineer."}, {"role": "user", "content": prompt}], "temperature": 0.2}
        try:
            r = requests.post(self.models["primary"]["endpoint"], json=data, headers=headers, timeout=30)
            return r.json()["choices"][0]["message"]["content"] if r.status_code == 200 else None
        except: return None

    def call_huggingface(self, model, prompt):
        headers = {"Authorization": f"Bearer {self.hf_token}", "Content-Type": "application/json"}
        data = {"inputs": f"<s>[INST] {prompt} [/INST]", "parameters": {"max_new_tokens": 500}}
        try:
            r = requests.post(model["endpoint"], json=data, headers=headers, timeout=60)
            return r.json()[0].get("generated_text", "") if r.status_code == 200 else None
        except: return None

    def generate_fix(self, prompt):
        if not self.active_model: return self.rule_based_fix(prompt)
        
        print(f"🤖 Using: {self.active_model['name']}")
        result = self.call_deepseek(prompt) if self.active_model["type"] == "api" else self.call_huggingface(self.active_model, prompt)
        
        if result: return result
        
        for key in ["fallback_1", "fallback_2"]:
            model = self.models[key]
            if model["available"]:
                print(f"🔄 Fallback to: {model['name']}")
                res = self.call_huggingface(model, prompt)
                if res: return res
        return self.rule_based_fix(prompt)

    def rule_based_fix(self, prompt):
        return "# Fallback Fix\ndef detect_niche(self, title, about, desc):\n    return 'general'"

if __name__ == "__main__":
    ai = MultiModelAI()
    print(json.dumps({"status": "ready", "active": ai.active_model["name"] if ai.active_model else "none"}, indent=2))
