import json
import os
import time
import google.generativeai as genai

# ==========================================
# وظائف التعامل مع ملفات JSON
# ==========================================

def load_json(file_path, default_data=None):
    """تحميل ملف JSON بأمان"""
    if default_data is None:
        default_data = {}
    if not os.path.exists(file_path):
        return default_data
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return default_data

def save_json(file_path, data):
    """حفظ بيانات JSON بأمان"""
    dir_name = os.path.dirname(file_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception:
        return False

# ==========================================
# وظائف الذكاء الاصطناعي وتوليد الصور
# ==========================================

def call_agent_with_retry(agent_function, *args, max_retries=3, delay=2, **kwargs):
    """دالة لإعادة محاولة الطلب تلقائياً عند انشغال السيرفر (503)"""
    for attempt in range(max_retries):
        try:
            return agent_function(*args, **kwargs)
        except Exception as e:
            error_msg = str(e)
            if "503" in error_msg or "UNAVAILABLE" in error_msg:
                if attempt < max_retries - 1:
                    time.sleep(delay * (attempt + 1))
                    continue
            raise e

def generate_image_safe(prompt):
    """دالة توليد الصور الآمنة مع معالجة الأخطاء"""
    def _generate():
        model = genai.GenerativeModel('imagen-3.0-generate-001')
        return model.generate_content(prompt)
    
    try:
        return call_agent_with_retry(_generate)
    except Exception as e:
        return f"عذراً، تعذر توليد الصورة حالياً: {e}"
