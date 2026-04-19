#!/usr/bin/env python3
"""
Test script to verify all Supabase connections and tables
"""

import os
import sys
import time
from supabase_connection import supabase_conn

def test_connection():
    print("=" * 50)
    print("Testing Supabase Connection")
    print("=" * 50)
    
    if not supabase_conn.is_connected():
        print("❌ Failed to connect to Supabase")
        print("   Check SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY")
        return False
    
    print("✅ Connected to Supabase")
    return True

def test_tables():
    print("\n" + "=" * 50)
    print("Testing Tables")
    print("=" * 50)
    
    tables_info = supabase_conn.get_all_tables_info()
    
    for table, info in tables_info.items():
        if info["exists"]:
            print(f"✅ {table}: exists (count: {info['count']})")
        else:
            print(f"❌ {table}: does not exist - run SQL script")
    
    return all(info["exists"] for info in tables_info.values())

def test_training_materials():
    print("\n" + "=" * 50)
    print("Testing Training Materials")
    print("=" * 50)
    
    # Test insert
    result = supabase_conn.save_training_material(
        "TEST_Connection",
        "This is a test entry to verify database connection"
    )
    
    if result:
        print("✅ Insert test passed")
    else:
        print("❌ Insert test failed")
        return False
    
    # Test retrieve
    materials = supabase_conn.get_training_materials(topic="TEST_Connection")
    print(f"✅ Retrieved {len(materials)} test records")
    
    return True

def test_generation_history():
    print("\n" + "=" * 50)
    print("Testing Generation History")
    print("=" * 50)
    
    test_input = {"test": "connection_test", "timestamp": time.time()}
    test_analyst = {"niche": "test", "status": "ok"}
    test_output = {"positive": "test prompt", "negative": "test negative"}
    
    result = supabase_conn.save_generation(test_input, test_analyst, test_output)
    
    if result:
        print("✅ Save generation test passed")
    else:
        print("❌ Save generation test failed")
        return False
    
    history = supabase_conn.get_generation_history(limit=5)
    print(f"✅ Retrieved {len(history)} generation records")
    
    return True

def test_chat_history():
    print("\n" + "=" * 50)
    print("Testing Chat History")
    print("=" * 50)
    
    conv_id = f"test_{int(time.time())}"
    
    result = supabase_conn.save_chat_message(
        conv_id,
        "Test user input",
        "Test AI response",
        "test_niche"
    )
    
    if result:
        print("✅ Save chat message test passed")
    else:
        print("❌ Save chat message test failed")
        return False
    
    history = supabase_conn.get_chat_history(conv_id)
    print(f"✅ Retrieved {len(history)} chat records")
    
    return True

def main():
    print("\n" + "=" * 60)
    print("SUPABASE CONNECTION TEST SUITE")
    print("=" * 60)
    
    results = []
    
    results.append(("Connection", test_connection()))
    results.append(("Tables", test_tables()))
    results.append(("Training Materials", test_training_materials()))
    results.append(("Generation History", test_generation_history()))
    results.append(("Chat History", test_chat_history()))
    
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("   Supabase connection is fully configured")
    else:
        print("⚠️ SOME TESTS FAILED")
        print("   Run supabase_schema.sql and supabase_testing_explorer.sql")
    print("=" * 50)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
