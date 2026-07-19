import os
import json
from datetime import datetime

class InferenceEngine:
    def __init__(self):
        # مسارات ملفات قاعدة المعرفة
        self.knowledge_path = "data/knowledge.json"
        self.memory_path = "data/conversation.json"
        
        # تحميل البيانات
        self.knowledge = self._load_json(self.knowledge_path) or {"coupons": []}
        self.memory = self._load_json(self.memory_path) or []

    def _load_json(self, path):
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return None
        return None

    def _save_json(self, path, data):
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def search(self, query):
        """
        دالة البحث الذكية: تبحث في الكلمات المفتاحية، المتاجر، الأكواد، والأوصاف
        """
        query = query.strip().lower()
        results = []
        
        # جلب قائمة الكوبونات والعروض
        coupons = self.knowledge.get("coupons", [])
        
        for item in coupons:
            match_found = False
            
            # 1. الفحص الذكي للكلمات المفتاحية (Keywords)
            keywords = item.get("keywords", [])
            for kw in keywords:
                kw = kw.lower()
                # إذا كانت الكلمة المفتاحية جزءاً من سؤال المستخدم (مثل: "السلام" داخل "السلام عليكم")
                if kw in query or query in kw:
                    match_found = True
                    break
            
            # 2. الفحص التقليدي (اسم المتجر، الكود، الوصف)
            store = item.get("store", "").lower()
            code = item.get("code", "").lower()
            desc = item.get("description", "").lower()
            
            if query in store or query in code or query in desc:
                match_found = True
                
            # إذا تطابق البحث، أضف العرض إلى النتائج
            if match_found:
                results.append(item)
                
        return results

    def add_coupon(self, store, code, description, keywords=None):
        if keywords is None:
            keywords = []
            
        new_coupon = {
            "store": store.strip(),
            "code": code.strip().upper(),
            "description": description.strip(),
            "keywords": keywords,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if "coupons" not in self.knowledge:
            self.knowledge["coupons"] = []
            
        self.knowledge["coupons"].append(new_coupon)
        return self._save_json(self.knowledge_path, self.knowledge)
