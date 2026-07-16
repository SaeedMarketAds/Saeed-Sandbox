import os
import json

def ensure_dir(path):
    """
    التأكد من وجود المجلد وإنشائه تلقائياً إذا لم يكن موجوداً.
    """
    if '.' in os.path.basename(path):
        path = os.path.dirname(path)
    
    if path and not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def save_json(file_path, data):
    """حفظ البيانات في ملف JSON"""
    ensure_dir(file_path)
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Error saving JSON: {e}")
        return False

def load_json(file_path):
    """تحميل البيانات من ملف JSON"""
    ensure_dir(file_path)
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return {}
