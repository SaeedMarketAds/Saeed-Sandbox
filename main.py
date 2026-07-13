import json
import streamlit as st

# دالة تحميل البيانات
def load_knowledge():
    try:
        with open('data/knowledge.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "ملف البيانات غير موجود"}

# واجهة المستخدم البسيطة
st.title("🧠 SaeeD LogiC")
user_input = st.text_input("اطرح سؤالك هنا:")

if user_input:
    knowledge = load_knowledge()
    response = "عذراً، لم أجد إجابة في قاعدة المعرفة."
    
    # البحث عن مفتاح مطابق
    for key, val in knowledge.items():
        if key in user_input.lower():
            response = val
            break
            
    st.write("الرد:", response)
