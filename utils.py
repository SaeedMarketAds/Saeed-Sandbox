import os

def save_json(path, data):
    # تحويل المسار إلى مسار مطلق لتجنب النصوص الفارغة
    absolute_path = os.path.abspath(path)
    dirname = os.path.dirname(absolute_path)
    
    # إنشاء المجلدات إن لم تكن موجودة
    os.makedirs(dirname, exist_ok=True)
    
    # بعد ذلك يمكنك فتح الملف والكتابة فيه بشكل طبيعي...
