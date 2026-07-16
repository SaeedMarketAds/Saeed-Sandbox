import os
import json

def save_json(path, data):
    """
    حفظ البيانات في ملف JSON مع معالجة أخطاء المسارات
    """
    try:
        # التأكد من وجود المجلد
        dir_path = os.path.dirname(path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        
        # حفظ الملف
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
        
    except Exception as e:
        print(f"⚠️ خطأ في حفظ الملف {path}: {e}")
        return False

def load_json(path):
    """
    تحميل البيانات من ملف JSON
    """
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # إنشاء ملف فارغ إذا لم يكن موجوداً
            save_json(path, {})
            return {}
            
    except Exception as e:
        print(f"⚠️ خطأ في تحميل الملف {path}: {e}")
        return {}

def ensure_directories():
    """
    التأكد من وجود جميع المجلدات المطلوبة
    """
    directories = ['data', 'memory']
    for dir_name in directories:
        dir_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), dir_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            print(f"✅ تم إنشاء المجلد: {dir_name}")
