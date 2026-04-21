#!/usr/bin/env python3
import os, json, re
from datetime import datetime
from pathlib import Path

class TaskManager:
    def __init__(self):
        self.status_file = ".github/task_status.json"
        self.alerts_file = ".github/alerts.log"
        self.load_status()
    
    def load_status(self):
        if os.path.exists(self.status_file):
            with open(self.status_file, 'r') as f: self.status = json.load(f)
        else:
            self.status = {"current_task": None, "completed_tasks": [], "pending_tasks": [], "blocked_tasks": [], "alerts": []}
    
    def save_status(self):
        with open(self.status_file, 'w') as f: json.dump(self.status, f, indent=2)
    
    def add_alert(self, level, title, message, requires_action=False):
        alert = {"timestamp": datetime.now().isoformat(), "level": level, "title": title, "message": message, "requires_action": requires_action, "resolved": False}
        self.status["alerts"].append(alert)
        with open(self.alerts_file, 'a') as f: f.write(f"[{alert['timestamp']}] [{level}] {title}: {message}\n")
        print(f"🔔 [{level}] {title}")
        return alert

    def check_api_keys(self):
        required = ["DEEPSEEK_API_KEY", "HF_TOKEN", "DOCKERHUB_USERNAME", "DOCKERHUB_TOKEN"]
        missing = [key for key in required if not os.environ.get(key)]
        if missing:
            self.add_alert("WARNING", "Missing API Keys", f"Required: {', '.join(missing)}", True)
            return False
        return True

    def parse_roadmap(self):
        tasks = []
        if os.path.exists("DNA.md"):
            with open("DNA.md", 'r') as f:
                content = f.read()
            versions = re.findall(r'### v([\d.]+).*?- (.+?)(?=\n\n|$)', content, re.DOTALL)
            for v, d in versions: tasks.append({"type": "version", "version": v, "description": d.strip(), "status": "pending"})
        return tasks

    def generate_report(self):
        return f"# 🤖 AI DevOps Report\nKeys: {'✅' if self.check_api_keys() else '⚠️'}\nAlerts: {len(self.status['alerts'])}"

if __name__ == "__main__":
    m = TaskManager()
    m.check_api_keys()
    task = m.parse_roadmap()
    print(m.generate_report())
