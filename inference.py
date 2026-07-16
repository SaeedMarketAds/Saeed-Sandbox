import os
import json
from .utils import save_json, load_json

class InferenceEngine:
    def __init__(self):
        # تحديد المسارات المطلقة
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.knowledge_path = os.path.join(base_dir, 'data', 'knowledge.json')
        self.memory_path = os.path.join(base_dir, 'memory', 'conversation.json')
        
        # تحميل المعرفة والذاكرة
        self.knowledge = load_json(self.knowledge_path)
        self.memory = load_json(self.memory_path)
        
        print("✅ تم تحميل محرك الذكاء الاصطناعي بنجاح")
    
    def answer(self, user_input):
        """
        معالجة سؤال المستخدم وإرجاع الإجابة
        """
        try:
            # البحث في المعرفة
            if user_input in self.knowledge:
                response = self.knowledge[user_input]
            else:
                # إجابة افتراضية للأسئلة غير المعروفة
                response = "⚠️ عفواً، لا أملك معلومات عن هذا السؤال حالياً. يمكنك إضافة الإجابة في ملف المعرفة."
            
            # حفظ المحادثة في الذاكرة
            self.memory[user_input] = {
                'response': response,
                'timestamp': str(__import__('datetime').datetime.now())
            }
            
            # حفظ الذاكرة
            save_json(self.memory_path, self.memory)
            
            return response
            
        except Exception as e:
            print(f"❌ خطأ في معالجة السؤال: {e}")
            return "عذراً، حدث خطأ أثناء معالجة سؤالك. يرجى المحاولة مرة أخرى."
    
    def add_knowledge(self, question, answer):
        """
        إضافة معرفة جديدة إلى النظام
        """
        self.knowledge[question] = answer
        return save_json(self.knowledge_path, self.knowledge)
    
    def get_memory(self):
        """
        استرجاع سجل المحادثات
        """
        return self.memory
