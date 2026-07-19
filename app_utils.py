import json
import os

def load_json(file_path, default=None):
    """تحميل ملف JSON بأمان"""
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return default or {}

def save_json(file_path, data):
    """حفظ بيانات JSON بأمان"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False
