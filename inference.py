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
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default

    def save_json(self, path, data):
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_response(self, user_input):
        user_input = user_input.lower().strip()
        best_match = None
        highest_score = 0
        
        # تحسين آلية مطابقة المعرفة بناءً على تداخل الكلمات (Score)
        for key, responses in self.knowledge.items():
            key_lower = key.lower()
            if key_lower in user_input:
                score = len(key_lower)  # كلما كانت الكلمة المفتاحية أطول وأدق زاد وزنها
                if score > highest_score:
                    highest_score = score
                    best_match = random.choice(responses)
        
        response = best_match if best_match else "عذراً، لم أجد إجابة مطابقة في قاعدة المعرفة المحلية حالياً."
        
        # تسجيل المحادثة تلقائياً
        self.log_conversation(user_input, response)
        return response

    def log_conversation(self, user_input, response):
        chat_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": user_input,
            "bot": response
        }
        self.history.append(chat_entry)
        self.save_json(self.history_path, self.history)
