import json
import os

class InferenceEngine:
    def __init__(self):
        # تحديد مسار ملف قاعدة البيانات المحلية داخل مجلد data
        self.json_path = os.path.join("data", "knowledge.json")
        self.knowledge_base = self.load_knowledge()
        
        # اسم ملف نموذج Gemma (بصيغة GGUF الخفيفة المخصصة للهواتف)
        # يجب تحميل الملف ووضعه في نفس مجلد المشروع
        self.model_path = "gemma-2-2b-it.Q4_K_M.gguf"
        self.model = None
        
        # تهيئة وتجهيز النموذج محلياً
        self.init_local_ai()

    def load_knowledge(self):
        """تحميل البيانات المحلية من ملف JSON بآمان"""
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def init_local_ai(self):
        """تحميل نموذج الذكاء الاصطناعي Gemma محلياً باستخدام مكتبة llama-cpp"""
        if os.path.exists(self.model_path):
            try:
                from llama_cpp import Llama
                # تحميل النموذج وتخصيص 4 خيوط معالجة تناسب معالجات الهواتف المتطورة
                self.model = Llama(
                    model_path=self.model_path,
                    n_ctx=2048,      # حجم سياق الذاكرة
                    n_threads=4      # عدد الأنوية المستخدمة من المعالج
                )
            except ImportError:
                print("تنبيه: مكتبة llama-cpp-python غير مثبتة بعد في بيئتك البرمجية.")
        else:
            print(f"تنبيه: ملف النموذج {self.model_path} غير موجود في المجلد الحالي.")

    def answer(self, question):
        """دالة الاستجابة الذكية الذكية (تبحث في JSON أولاً ثم تنتقل لـ Gemma)"""
        question_clean = question.strip().lower()
        
        # 1. المرحلة الأولى: البحث الذكي السريع في ملف الـ JSON الخاص بك (لتوفير الوقت وموارد الهاتف)
        for key, value in self.knowledge_base.items():
            if key.lower() in question_clean or question_clean in key.lower():
                return f"📢 الإجابة من قاعدة البيانات المحلية:\n\n{value}"
        
        # 2. المرحلة الثانية: إذا لم يجد إجابة مطابقة، يتدخل ذكاء غيما (Gemma) ليصيغ الرد
        if self.model:
            # بناء أمر برمي (Prompt) يوجه النموذج للرد بالعربية وبطريقة احترافية
            prompt = f"<start_of_turn>user\nأنت مساعد ذكي مدمج في نظام Saeed Logic. أجب على السؤال التالي بلغة عربية سليمة وموجزة:\n{question}<end_of_turn>\n<start_of_turn>model\n"
            try:
                output = self.model(
                    prompt, 
                    max_tokens=200, 
                    stop=["<end_of_turn>"], 
                    echo=False
                )
                return output['choices'][0]['text'].strip()
            except Exception as e:
                return f"❌ حدث خطأ أثناء تشغيل معالجة الذكاء الاصطناعي: {e}"
        
        # خيار احتياطي في حال عدم تحميل الموديل وعدم وجود إجابة في الـ JSON
        return "🤖 عذراً، لم أجد إجابة مطابقة في قاعدة البيانات المحلية، ولم يتم تفعيل محرك Gemma الذكي (تأكد من تحميل ملف الـ GGUF الخاص بالنموذج)."

    def add_knowledge(self, question, answer):
        """إضافة معرفة جديدة إلى ملف JSON وحفظها فوراً"""
        self.knowledge_base[question] = answer
        try:
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(self.knowledge_base, f, ensure_ascii=False, indent=4)
            return True
        except:
            return False
