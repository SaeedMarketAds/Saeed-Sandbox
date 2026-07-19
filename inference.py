import os
import json
from datetime import datetime

class InferenceEngine:
    def __init__(self):
        # الاعتماد على المسارات الموحدة داخل مجلد data
        self.knowledge_path = "data/knowledge.json"
        self.memory_path = "data/conversation.json"
        
        self.knowledge = self._load_json(self.knowledge_path) or {"coupons": [], "offers": []}
        self.memory = self._load_json(self.memory_path) or []

    def _load_json(self, path):
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return None
        return None

    def _save_json(self, path, data):
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def search(self, search_term):
        """البحث في الكوبونات المخزنة بناءً على اسم المتجر أو الكود أو الوصف"""
        term = search_term.lower().strip()
        results = {"coupons": []}
        
        for coupon in self.knowledge.get("coupons", []):
            if (term in coupon.get("store", "").lower() or 
                term in coupon.get("code", "").lower() or 
                term in coupon.get("description", "").lower()):
                results["coupons"].append(coupon)
        
        # تسجيل عملية البحث في سجل الذاكرة والمحادثات
        self._log_conversation("user", f"بحث عن: {search_term}")
        self._log_conversation("assistant", f"تم العثور على {len(results['coupons'])} نتيجة")
        
        return results if results["coupons"] else None

    def add_coupon(self, store, code, description, link=""):
        """إضافة كوبون جديد إلى ملف البيانات واعادة حفظه"""
        new_coupon = {
            "store": store.strip(),
            "code": code.strip().upper(),
            "description": description.strip(),
            "link": link.strip(),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        if "coupons" not in self.knowledge:
            self.knowledge["coupons"] = []
            
        self.knowledge["coupons"].append(new_coupon)
        
        # تسجيل الحدث في الذاكرة
        self._log_conversation("system", f"إضافة كوبون لمتجر: {store.strip()}")
        
        return self._save_json(self.knowledge_path, self.knowledge)

    def get_all_coupons(self):
        """جلب كافة الكوبونات المتوفرة"""
        return self.knowledge.get("coupons", [])

    def delete_coupon(self, index):
        """حذف كوبون محدد بناءً على موقعه (index)"""
        try:
            if "coupons" in self.knowledge and 0 <= index < len(self.knowledge["coupons"]):
                removed = self.knowledge["coupons"].pop(index)
                self._log_conversation("system", f"حذف كوبون لمتجر: {removed.get('store')}")
                return self._save_json(self.knowledge_path, self.knowledge)
            return False
        except Exception:
            return False

    def get_conversations(self):
        """جلب سجل النشاط والمحادثات"""
        return self.memory

    def _log_conversation(self, role, content):
        """دالة داخلية لتسجيل الحركات والمحادثات في ملف conversation.json"""
        log_entry = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.memory.append(log_entry)
        self._save_json(self.memory_path, self.memory)
