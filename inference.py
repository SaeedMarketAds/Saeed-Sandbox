import json
import os
import random
from datetime import datetime

class InferenceEngine:
    def __init__(self, knowledge_path="data/knowledge.json", history_path="conversation.json"):
        self.knowledge_path = knowledge_path
        self.history_path = history_path
        self.knowledge = self.load_json(self.knowledge_path, default={})
        self.history = self.load_json(self.history_path, default=[])

    def load_json(self, path, default):
        """قراءة ملفات JSON بأمان مع دعم الترميز العربي"""
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return default
        return default

    def save_json(self, path, data):
        """حفظ ملفات JSON وإنشاء المجلدات إذا لم تكن موجودة"""
        try:
            dir_name = os.path.dirname(path)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"خطأ أثناء الحفظ: {e}")

    def get_response(self, user_input):
        """البحث عن أفضل رد مطابِق بناءً على الكلمات المفتاحية"""
        user_input = user_input.lower().strip()
        best_match = None
        highest_score = 0
        
        # آلية مطابقة ذكية تعتمد على طول الكلمة المفتاحية لضمان الدقة
        for key, responses in self.knowledge.items():
            key_lower = key.lower()
            if key_lower in user_input:
                score = len(key_lower)
                if score > highest_score:
                    highest_score = score
                    best_match = random.choice(responses)
        
        response = best_match if best_match else "عذراً، لم أجد إجابة مطابقة في قاعدة المعرفة المحلية حالياً."
        
        # تسجيل المحادثة تلقائياً في السجل
        self.log_conversation(user_input, response)
        return response

    def log_conversation(self, user_input, response):
        """إضافة المحادثة الحالية وتحديث ملف الهستوري"""
        chat_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": user_input,
            "bot": response
        }
        self.history.append(chat_entry)
        self.save_json(self.history_path, self.history)
