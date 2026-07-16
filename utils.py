import os
import json

def save_json(path, data):
    # 1. الحصول على مسار المجلد الحالي للمشروع بدقة
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. تنظيف اسم الملف (أخذ الاسم فقط إذا كان مساراً نسبياً مضطرباً)
    file_name = os.path.basename(path) if not path.endswith(('.json', '.txt')) else path
    
    # 3. دمج المسار ليصبح مطلقاً وواضحاً للسيرفر
    if not os.path.isabs(file_name):
        full_path = os.path.join(current_dir, file_name)
    else:
        full_path = file_name

    # 4. استخراج المجلد الأب وإنشائه بأمان
    dirname = os.path.dirname(full_path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    
    # 5. حفظ البيانات
    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
