import os
import json
from supabase import create_client, Client
from datetime import datetime
import uuid

class SupabaseManager:
    def __init__(self):
        self.url = os.environ.get("SUPABASE_URL")
        self.key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        self.client = None
        if self.url and self.key:
            self.client = create_client(self.url, self.key)
    
    def is_connected(self):
        return self.client is not None
    
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
            print(f"Supabase error: {e}")
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
            print(f"Supabase error: {e}")
            return []
    
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
            print(f"Supabase error: {e}")
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
            print(f"Supabase error: {e}")
            return []
    
    def save_chat_history(self, conversation_id, user_input, ai_response, niche):
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
            print(f"Supabase error: {e}")
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
            print(f"Supabase error: {e}")
            return []
    
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
            print(f"Supabase error: {e}")
            return False

supabase_manager = SupabaseManager()
