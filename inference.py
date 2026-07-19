import json
import os
from datetime import datetime

class InferenceEngine:
    def __init__(self):
        self.knowledge_path = "data/knowledge.json"
        self.conversation_path = "data/conversation.json"
        self.load_data()
    
    def load_data(self):
        """تحميل البيانات من الملفات"""
        try:
            with open(self.knowledge_path, "r", encoding="utf-8") as f:
                self.knowledge = json.load(f)
        except:
            self.knowledge = {"coupons": [], "offers": []}
        
        try:
            with open(self.conversation_path, "r", encoding="utf-8") as f:
                self.conversations = json.load(f)
        except:
            self.conversations = []
    
    def save_data(self):
        """حفظ البيانات في الملفات"""
        with open(self.knowledge_path, "w", encoding="utf-8") as f:
            json.dump(self.knowledge, f, ensure_ascii=False, indent=2)
        
        with open(self.conversation_path, "w", encoding="utf-8") as f:
            json.dump(self.conversations, f, ensure_ascii=False, indent=2)
    
    def search(self, query):
        """البحث عن عروض أو كوبونات مطابقة"""
        results = []
        query_lower = query.lower()
        
        for coupon in self.knowledge.get("coupons", []):
            if (query_lower in coupon.get("store", "").lower() or
                query_lower in coupon.get("code", "").lower() or
                query_lower in coupon.get("description", "").lower()):
                results.append(coupon)
        
        # تسجيل المحادثة
        self.conversations.append({
            "role": "user",
            "content": query,
            "timestamp": datetime.now().isoformat()
        })
        self.conversations.append({
            "role": "assistant",
            "content": f"تم العثور على {len(results)} نتيجة",
            "timestamp": datetime.now().isoformat()
        })
        self.save_data()
        
        return results if results else None
    
    def add_coupon(self, store, code, description, link=""):
        """إضافة كوبون جديد"""
        try:
            new_coupon = {
                "store": store,
                "code": code,
                "description": description,
                "link": link,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            
            self.knowledge["coupons"].append(new_coupon)
            self.save_data()
            return True
        except:
            return False
    
    def get_all_coupons(self):
        """الحصول على جميع الكوبونات"""
        return self.knowledge.get("coupons", [])
    
    def delete_coupon(self, index):
        """حذف كوبون حسب الفهرس"""
        try:
            if 0 <= index < len(self.knowledge["coupons"]):
                del self.knowledge["coupons"][index]
                self.save_data()
                return True
            return False
        except:
            return False
    
    def get_conversations(self):
        """الحصول على سجل المحادثات"""
        return self.conversations
