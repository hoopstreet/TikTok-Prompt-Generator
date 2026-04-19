#!/usr/bin/env python3
"""
Supabase Initialization Script
Run this once to verify connection and insert training materials
"""

import os
import sys
from supabase_config import supabase_manager

def init_training_materials():
    training_data = [
        {
            "topic": "Universal_Affiliate_Logic",
            "content": "Follow the 15s/5-shot density. Use Taglish 'Budol' tone. No store names. Output 4 cards: Info, Brief, Analysis, Storyboard."
        },
        {
            "topic": "TikTok_Vibe",
            "content": "Keep the tone casual, high-energy, and relatable. Use Gen Z slang sparingly but effectively."
        },
        {
            "topic": "Hook_Styles",
            "content": "Always start with a strong visual hook: 'I wish I knew this before...' or 'Stop scrolling if you want to save money on...'"
        },
        {
            "topic": "CTA_Format",
            "content": "The end must always mention the Yellow Basket: 'Check the yellow basket below to grab yours before it runs out!'"
        }
    ]
    
    print("Inserting training materials...")
    for data in training_data:
        result = supabase_manager.save_training_material(data["topic"], data["content"])
        if result:
            print(f"  ✓ Inserted: {data['topic']}")
        else:
            print(f"  ✗ Failed: {data['topic']}")

def verify_connection():
    print("Verifying Supabase connection...")
    if supabase_manager.is_connected():
        print("  ✓ Connected to Supabase")
        return True
    else:
        print("  ✗ Failed to connect. Check SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Supabase Initialization")
    print("=" * 50)
    
    if verify_connection():
        init_training_materials()
        print("\n" + "=" * 50)
        print("Initialization complete!")
    else:
        print("\nPlease set environment variables:")
        print("  SUPABASE_URL")
        print("  SUPABASE_SERVICE_ROLE_KEY")
        sys.exit(1)
