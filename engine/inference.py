import json
import os

def search_knowledge_base(user_query, json_path="data/knowledge.json"):
    """
    دالة ذكية تقرأ قاعدة المعرفة وتبحث عن الإجابة المتوافقة مع سؤال المستخدم.
    """
    # التأكد من وجود الملف أولاً
    if not os.path.exists(json_path):
        return "عذراً، ملف قاعدة المعرفة غير موجود حالياً."

    try:
        # قراءة البيانات من ملف JSON
        with open(json_path, 'r', encoding='utf-8') as file:
            knowledge_data = json.load(file)
        
        # تحويل سؤال المستخدم إلى أحرف صغيرة المقارنة (إذا كانت بالإنجليزية) أو تنظيف النص
        query = user_query.strip().lower()
        
        # البحث داخل قاعدة المعرفة (افترضنا أن الهيكل يحتوي على سؤال وجواب)
        # يمكنك تعديل طريقة البحث حسب هيكلة الـ JSON لديك (مثلاً: الكلمات المفتاحية)
        for item in knowledge_data:
            if query in item.get("question", "").lower() or query in item.get("keywords", ""):
                return item.get("answer", "تم العثور على القسم، ولكن لا توجد إجابة محددة.")
        
        # اللمسة الذكية: إذا مر على كل البيانات ولم يجد إجابة متطابقة
        return "أنا مبرمج للإجابة بناءً على قاعدة المعرفة الخاصة بالعروض والكوبونات فقط، وللأسف لا أملك إجابة على هذا السؤال حالياً! 🤖"

    except Exception as e:
        return f"حدث خطأ أثناء محاولة قراءة قاعدة المعرفة: {str(e)}"
