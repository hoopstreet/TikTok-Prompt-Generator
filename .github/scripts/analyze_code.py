#!/usr/bin/env python3
"""
AI Code Analyzer - Scans entire repository
"""

import os
import json
import ast
from datetime import datetime

def analyze_app_py():
    """Analyze app.py for issues"""
    issues = []
    if not os.path.exists('app.py'):
        return [{"error": "app.py not found"}]
    
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Check imports
    if 'import gradio' not in content:
        issues.append({"type": "missing_import", "module": "gradio"})
    
    # Check class
    if 'class AITrainingCore' not in content:
        issues.append({"type": "missing_class", "class": "AITrainingCore"})
    
    # Check methods
    required_methods = ['detect_niche', 'generate']
    for method in required_methods:
        if f'def {method}' not in content:
            issues.append({"type": "missing_method", "method": method})
    
    return issues

def analyze_dna_md():
    """Check DNA.md completeness"""
    issues = []
    if not os.path.exists('DNA.md'):
        return [{"error": "DNA.md not found"}]
    
    with open('DNA.md', 'r') as f:
        content = f.read()
    
    if 'AI_TRAINING_CORE' not in content:
        issues.append({"type": "missing_section", "section": "AI_TRAINING_CORE"})
    
    return issues

def main():
    report = {
        "timestamp": datetime.now().isoformat(),
        "app_issues": analyze_app_py(),
        "dna_issues": analyze_dna_md(),
        "total_issues": 0
    }
    
    report["total_issues"] = len(report["app_issues"]) + len(report["dna_issues"])
    
    with open('analysis_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"✅ Analysis complete: {report['total_issues']} issues found")

if __name__ == "__main__":
    main()
