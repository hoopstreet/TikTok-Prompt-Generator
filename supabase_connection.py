"""
Supabase Connection Configuration for TikTok-Prompt-Generator
Handles all database operations for:
- generation_history
- training_materials  
- chat_history
- testing_explorer
"""

import os
import json
import uuid
from datetime import datetime
from supabase import create_client, Client

class SupabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self.url = os.environ.get("SUPABASE_URL")
        self.key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        self.client = None
        if self.url and self.key:
            self.client = create_client(self.url, self.key)
        self._initialized = True
    
    def is_connected(self):
        return self.client is not None
    
    # =============================================
    # GENERATION HISTORY METHODS
    # =============================================
    def save_generation(self, input_field, analyst_product, final_output):
        if not self.client:
            return False
        try:
            data = {
                "id": str(uuid.uuid4()),
                "input_field": input_field,
                "analyst_product": analyst_product,
                "final_output": final_output,
                "created_at": datetime.now().isoformat()
            }
            result = self.client.table("generation_history").insert(data).execute()
            return True
        except Exception as e:
            print(f"Save generation error: {e}")
            return False
    
    def get_generation_history(self, limit=100):
        if not self.client:
            return []
        try:
            result = self.client.table("generation_history")\
                .select("*")\
                .order("created_at", desc=True)\
                .limit(limit)\
                .execute()
            return result.data
        except Exception as e:
            print(f"Get generation history error: {e}")
            return []
    
    def delete_generation(self, record_id):
        if not self.client:
            return False
        try:
            result = self.client.table("generation_history")\
                .delete()\
                .eq("id", record_id)\
                .execute()
            return True
        except Exception as e:
            print(f"Delete generation error: {e}")
            return False
    
    # =============================================
    # TRAINING MATERIALS METHODS
    # =============================================
    def save_training_material(self, topic, content):
        if not self.client:
            return False
        try:
            data = {
                "id": str(uuid.uuid4()),
                "topic": topic,
                "content": content,
                "created_at": datetime.now().isoformat()
            }
            result = self.client.table("training_materials").insert(data).execute()
            return True
        except Exception as e:
            print(f"Save training material error: {e}")
            return False
    
    def get_training_materials(self, topic=None):
        if not self.client:
            return []
        try:
            query = self.client.table("training_materials").select("*")
            if topic:
                query = query.eq("topic", topic)
            result = query.order("created_at", desc=True).execute()
            return result.data
        except Exception as e:
            print(f"Get training materials error: {e}")
            return []
    
    def update_training_material(self, record_id, topic, content):
        if not self.client:
            return False
        try:
            data = {"topic": topic, "content": content}
            result = self.client.table("training_materials")\
                .update(data)\
                .eq("id", record_id)\
                .execute()
            return True
        except Exception as e:
            print(f"Update training material error: {e}")
            return False
    
    def delete_training_material(self, record_id):
        if not self.client:
            return False
        try:
            result = self.client.table("training_materials")\
                .delete()\
                .eq("id", record_id)\
                .execute()
            return True
        except Exception as e:
            print(f"Delete training material error: {e}")
            return False
    
    # =============================================
    # CHAT HISTORY METHODS (Memory)
    # =============================================
    def save_chat_message(self, conversation_id, user_input, ai_response, niche):
        if not self.client:
            return False
        try:
            data = {
                "id": str(uuid.uuid4()),
                "conversation_id": conversation_id,
                "user_input": user_input,
                "ai_response": ai_response,
                "niche": niche,
                "created_at": datetime.now().isoformat()
            }
            result = self.client.table("chat_history").insert(data).execute()
            return True
        except Exception as e:
            print(f"Save chat message error: {e}")
            return False
    
    def get_chat_history(self, conversation_id, limit=10):
        if not self.client:
            return []
        try:
            result = self.client.table("chat_history")\
                .select("*")\
                .eq("conversation_id", conversation_id)\
                .order("created_at", desc=True)\
                .limit(limit)\
                .execute()
            return result.data
        except Exception as e:
            print(f"Get chat history error: {e}")
            return []
    
    def get_last_n_messages(self, conversation_id, n=3):
        history = self.get_chat_history(conversation_id, limit=n)
        return list(reversed(history))
    
    def delete_old_chat_history(self, days=30):
        if not self.client:
            return False
        try:
            from datetime import datetime, timedelta
            cutoff = (datetime.now() - timedelta(days=days)).isoformat()
            result = self.client.table("chat_history")\
                .delete()\
                .lt("created_at", cutoff)\
                .execute()
            return True
        except Exception as e:
            print(f"Delete old chat history error: {e}")
            return False
    
    # =============================================
    # TESTING EXPLORER METHODS
    # =============================================
    def save_test_result(self, test_name, test_input, test_output, status, duration_ms):
        if not self.client:
            return False
        try:
            data = {
                "id": str(uuid.uuid4()),
                "test_name": test_name,
                "test_input": test_input,
                "test_output": test_output,
                "status": status,
                "duration_ms": duration_ms,
                "created_at": datetime.now().isoformat()
            }
            result = self.client.table("testing_explorer").insert(data).execute()
            return True
        except Exception as e:
            print(f"Save test result error: {e}")
            return False
    
    def get_test_results(self, limit=50):
        if not self.client:
            return []
        try:
            result = self.client.table("testing_explorer")\
                .select("*")\
                .order("created_at", desc=True)\
                .limit(limit)\
                .execute()
            return result.data
        except Exception as e:
            print(f"Get test results error: {e}")
            return []
    
    def get_test_stats(self):
        if not self.client:
            return {}
        try:
            result = self.client.table("testing_explorer")\
                .select("status", count="exact")\
                .execute()
            total = len(result.data)
            passed = len([r for r in result.data if r.get("status") == "passed"])
            failed = len([r for r in result.data if r.get("status") == "failed"])
            return {"total": total, "passed": passed, "failed": failed}
        except Exception as e:
            print(f"Get test stats error: {e}")
            return {}
    
    # =============================================
    # UTILITY METHODS
    # =============================================
    def get_all_tables_info(self):
        if not self.client:
            return {}
        tables = ["generation_history", "training_materials", "chat_history", "testing_explorer"]
        info = {}
        for table in tables:
            try:
                result = self.client.table(table).select("*", count="exact").limit(0).execute()
                info[table] = {"count": result.count if hasattr(result, 'count') else 0, "exists": True}
            except:
                info[table] = {"count": 0, "exists": False}
        return info

# Singleton instance
supabase_conn = SupabaseConnection()
