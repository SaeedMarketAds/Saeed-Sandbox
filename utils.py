import os
import json

def save_json(path, data):
    # استخراج اسم الملف فقط (مثل memory.json) وتجاهل أي مسارات فرعية مكسورة
    file_name = os.path.basename(path) if path else "memory.json"
    
    # تحديد مسار المجلد الحالي للمشروع بدقة على سيرفر Streamlit
    current_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(current_dir, file_name)
    
    # حفظ الملف مباشرة بدون الحاجة لإنشاء مجلدات جديدة
    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
