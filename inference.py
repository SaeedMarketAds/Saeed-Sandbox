import os
import json
# بدلاً من الاستيراد القديم
from app_utils import save_json, load_json


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
        معالجة سؤال المستخدم وإرجاع الإجابة بتصفية ذكية لكلمات السؤال
        """
        try:
            # 1. تنظيف علامات الاستفهام والمسافات الزائدة
            cleaned_input = user_input.strip().replace("؟", "").replace("?", "")
            
            # قائمة الكلمات والأدوات الشائعة لتجاهلها والوصول لجوهر السؤال
            stop_words = ["من هو", "ماهو", "ما هو", "ما هي", "ماهي", "ايش هو", "ايش", "هو", "هي", "شو"]
            
            # دالة داخلية لتنظيف النص من كلمات السؤال الزائدة
            def remove_question_words(text):
                txt = text
                for word in stop_words:
                    txt = txt.replace(word, "")
                return txt.strip()
            
            # استخراج الكلمة الأساسية من سؤال الزبون (مثال: "سعيد ماركت")
            core_input = remove_question_words(cleaned_input)
            response = None
            
            # 2. البحث عن تطابق دقيق أولاً
            if cleaned_input in self.knowledge:
                response = self.knowledge[cleaned_input]
            else:
                # 3. المطابقة الذكية عبر الكلمات الجوهرية
                for key in self.knowledge:
                    cleaned_key = key.strip().replace("؟", "").replace("?", "")
                    # استخراج الكلمة الأساسية من الجملة المدربة مخزناً
                    core_key = remove_question_words(cleaned_key)
                    
                    # التحقق من تشابه الجوهر (إذا كانت الكلمة الأساسية متطابقة)
                    if core_key and (core_key in core_input or core_input in core_key):
                        response = self.knowledge[key]
                        break
            
            # 4. إذا لم يجد البوت أي تطابق
            if response is None:
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
