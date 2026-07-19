import os
import json

def ensure_dir(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)

def load_json(file_path, default_data=None):
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
    dir_name = os.path.dirname(file_path)
    if dir_name:
        ensure_dir(dir_name)
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception:
        return False
