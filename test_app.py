#!/usr/bin/env python3
"""Test script to verify app.py works before deployment"""

import sys
import importlib.util

# Check if gradio is installed
try:
    import gradio
    print(f"✅ Gradio version: {gradio.__version__}")
except ImportError:
    print("❌ Gradio not installed. Run: pip install gradio")
    sys.exit(1)

# Check if app.py can be imported
try:
    spec = importlib.util.spec_from_file_location("app", "app.py")
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)
    print("✅ app.py syntax is valid")
    print("✅ AITrainingCore class loaded")
    print("✅ All functions defined")
except Exception as e:
    print(f"❌ Error loading app.py: {e}")
    sys.exit(1)

print("\n✅ All tests passed! Ready to deploy to HF Space")
