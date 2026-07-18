import os
import json
from utils import load_json, save_json, ensure_dir

# نحاول استيراد مكتبة ollama، وإذا لم تكن مثبتة نعطي رسالة واضحة بدل انهيار البرنامج
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


class InferenceEngine:
    def __init__(self, model_name: str = "deepseek-r1:1.5b"):
        # اسم النموذج المستخدم عبر Ollama (يمكن تغييره لاحقاً من الواجهة إن أردت)
        self.model_name = model_name

        # تحديد مسارات الملفات والمجلدات
        self.data_dir = "data"
        self.memory_dir = "memory"
        ensure_dir(self.data_dir)
        ensure_dir(self.memory_dir)

        self.knowledge_file = os.path.join(self.data_dir, "knowledge.json")

        # كلمات ترحيبية افتراضية يبدأ بها التطبيق (تُستخدم كسياق مساعد فقط الآن، وليست إجابة مباشرة)
        default_knowledge = {
            "السلام عليكم": "وعليكم السلام ورحمة الله وبركاته! أهلاً بك في نظام Saeed Logic الذكي.",
            "من أنت": "أنا Saeed Logic، نظام ذكاء اصطناعي محلي ومطور مخصص لمساعدتك في إدارة أعمالك الذكية بالكامل بدون إنترنت.",
            "مرحبا": "أهلاً وسهلاً بك! سعيد جداً بخدمتك اليوم.",
            "كيف حالك": "الحمد لله بأفضل حال! أتمنى أن تكون أنت وعملك في أتم الصحة والنجاح."
        }
        self.knowledge = load_json(self.knowledge_file, default_knowledge)

        # حفظ المعرفة الافتراضية إن لم يكن الملف موجوداً من قبل
        if not os.path.exists(self.knowledge_file):
            save_json(self.knowledge_file, self.knowledge)

    def _build_prompt(self, question: str) -> str:
        """يبني نص التوجيه (prompt) الذي يُرسل للنموذج، مدمجاً فيه قاعدة المعرفة المحلية كسياق."""
        return f"""أنت مساعد ذكي اسمه "Saeed Logic"، تتحدث العربية بطلاقة وبأسلوب ودود ومباشر.
استخدم البيانات المحلية التالية (إن كانت ذات صلة بالسؤال) كمرجع أساسي للإجابة.
إذا لم تكن هذه البيانات كافية، استخدم معرفتك العامة لتقديم إجابة مفيدة وصحيحة.
لا تذكر أنك تستخدم "بيانات محلية" في ردك، فقط أجب بشكل طبيعي.

البيانات المحلية المتوفرة (JSON):
{json.dumps(self.knowledge, ensure_ascii=False)}

سؤال المستخدم: {question}

الإجابة:"""

    def answer(self, question: str) -> str:
        """يولّد إجابة عبر نموذج DeepSeek المحلي (Ollama)، مستعيناً بقاعدة المعرفة كسياق."""
        if not question or not question.strip():
            return "يرجى كتابة سؤال أولاً."

        if not OLLAMA_AVAILABLE:
            return (
                "⚠️ مكتبة ollama غير مثبتة على هذا الجهاز.\n"
                "ثبّتها عبر: pip install ollama\n"
                "وتأكد أن تطبيق Ollama يعمل محلياً وأن النموذج "
                f"'{self.model_name}' تم تحميله عبر: ollama pull {self.model_name}"
            )

        prompt = self._build_prompt(question.strip())

        try:
            response = ollama.generate(model=self.model_name, prompt=prompt)
            text = response.get("response", "").strip()
            return text if text else "لم أتمكن من توليد إجابة، حاول صياغة السؤال بشكل مختلف."
        except Exception as e:
            return (
                "❌ تعذر الاتصال بنموذج Ollama المحلي.\n"
                f"تفاصيل الخطأ: {e}\n\n"
                "تأكد من:\n"
                "1) تشغيل تطبيق/خدمة Ollama على جهازك.\n"
                f"2) تحميل النموذج مسبقاً بالأمر: ollama pull {self.model_name}"
            )

    def add_knowledge(self, question: str, answer_text: str) -> bool:
        """إضافة سؤال وإجابة جديدة لقاعدة المعرفة المحلية (تُستخدم كسياق للنموذج لاحقاً)."""
        if not question or not answer_text:
            return False

        self.knowledge[question.strip()] = answer_text.strip()
        return save_json(self.knowledge_file, self.knowledge)
