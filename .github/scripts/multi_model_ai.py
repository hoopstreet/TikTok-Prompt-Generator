#!/usr/bin/env python3
import os, json, requests
from datetime import datetime

class MultiModelAI:
    def __init__(self):
        self.deepseek_api_key = os.environ.get("DEEPSEEK_API_KEY")
        self.hf_token = os.environ.get("HF_TOKEN")
        self.models = {
            "primary_api": {"name": "DeepSeek Coder (API)", "type": "api", "provider": "deepseek", "endpoint": "https://api.deepseek.com/v1/chat/completions", "available": bool(self.deepseek_api_key), "priority": 1},
            "primary_hf": {"name": "DeepSeek Coder (HF)", "type": "huggingface", "provider": "deepseek", "endpoint": "https://api-inference.huggingface.co/models/deepseek-ai/deepseek-coder-1.3b-base", "available": bool(self.hf_token), "priority": 2},
            "fallback_1": {"name": "CodeLlama 7B", "type": "huggingface", "provider": "meta", "endpoint": "https://api-inference.huggingface.co/models/codellama/CodeLlama-7b-hf", "available": bool(self.hf_token), "priority": 3},
            "fallback_2": {"name": "StarCoder2 3B", "type": "huggingface", "provider": "bigcode", "endpoint": "https://api-inference.huggingface.co/models/bigcode/starcoder2-3b", "available": bool(self.hf_token), "priority": 4}
        }
        self.active_model = self.select_best_model()

    def select_best_model(self):
        sorted_models = sorted(self.models.values(), key=lambda x: x["priority"])
        for model in sorted_models:
            if model["available"]: return model
        return None

    def call_deepseek_api(self, prompt):
        headers = {"Authorization": f"Bearer {self.deepseek_api_key}", "Content-Type": "application/json"}
        data = {"model": "deepseek-coder", "messages": [{"role": "user", "content": prompt}], "temperature": 0.2}
        try:
            r = requests.post(self.models["primary_api"]["endpoint"], json=data, headers=headers, timeout=30)
            return r.json()["choices"][0]["message"]["content"] if r.status_code == 200 else None
        except: return None

    def call_huggingface(self, model, prompt):
        headers = {"Authorization": f"Bearer {self.hf_token}", "Content-Type": "application/json"}
        formatted = prompt if model["provider"] == "deepseek" else f"<s>[INST] {prompt} [/INST]"
        data = {"inputs": formatted, "parameters": {"max_new_tokens": 500, "temperature": 0.2}}
        try:
            r = requests.post(model["endpoint"], json=data, headers=headers, timeout=60)
            if r.status_code == 200:
                res = r.json()
                return res[0].get("generated_text", "") if isinstance(res, list) else str(res)
            return None
        except: return None

    def generate_fix(self, prompt):
        if not self.active_model: return self.rule_based_fix(prompt)
        res = self.call_deepseek_api(prompt) if self.active_model["type"] == "api" else self.call_huggingface(self.active_model, prompt)
        if res: return res
        
        # Priority Fallback Chain
        for m in sorted(self.models.values(), key=lambda x: x["priority"]):
            if m != self.active_model and m["available"]:
                res = self.call_deepseek_api(prompt) if m["type"] == "api" else self.call_huggingface(m, prompt)
                if res: return res
        return self.rule_based_fix(prompt)

    def rule_based_fix(self, prompt):
        return "# Rule-based Fallback Active\ndef detect_niche(self, title, about, desc):\n    # Expanded Hoopstreet Niche Logic\n    return 'general'"

    def get_status_report(self):
        return {"timestamp": datetime.now().isoformat(), "active": self.active_model["name"] if self.active_model else "none"}

if __name__ == "__main__":
    ai = MultiModelAI()
    print(json.dumps(ai.get_status_report(), indent=2))
