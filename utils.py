import os
import json

def save_json(path, data):
    # 1. تحويل المسار إلى مسار مطلق لتجنب النصوص الفارغة والأخطاء على سيرفر Streamlit
    absolute_path = os.path.abspath(path)
    dirname = os.path.dirname(absolute_path)
    
    # 2. إنشاء المجلدات تلقائياً إن لم تكن موجودة
    os.makedirs(dirname, exist_ok=True)
    
    # 3. فتح الملف وحفظ البيانات بصيغة JSON
    with open(absolute_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
