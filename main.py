
import streamlit as st
import os
from inference import InferenceEngine

# 1. تعريف الدالة محلياً لتجنب خطأ NameError تماماً
def ensure_directories():
    """التأكد من إنشاء مجلدات البيانات والذاكرة تلقائياً"""
    os.makedirs("data", exist_ok=True)
    os.makedirs("memory", exist_ok=True)

# 2. استدعاء الدالة لتهيئة المجلدات (السطر 21)
ensure_directories()

# 3. تكميل بقية كود التطبيق...

# إعداد واجهة المستخدم
st.set_page_config(
    page_title="Saeed Logic - AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# عنوان التطبيق
st.title("🤖 Saeed Logic")
st.markdown("**بدون مفاتيح، API ذكاء اصطناعي محلي 100% — بدون إنتزنت**")

# إدخال السؤال
user_input = st.text_input("اطرح سؤالك هنا:", placeholder="اكتب سؤالك...")

if user_input:
    with st.spinner("جاري التفكير..."):
        # الحصول على الإجابة
        answer = st.session_state.engine.answer(user_input)
    
    # عرض الإجابة
    st.success("📝 الإجابة:")
    st.write(answer)
    
    # عرض سجل المحادثة (اختياري)
    with st.expander("📜 عرض سجل المحادثات"):
        memory = st.session_state.engine.get_memory()
        if memory:
            for question, data in list(memory.items())[-5:]:  # آخر 5 محادثات
                st.write(f"**س:** {question}")
                st.write(f"**ج:** {data['response']}")
                st.write(f"🕐 {data['timestamp']}")
                st.divider()
        else:
            st.info("لا توجد محادثات مسجلة بعد")

# زر لإضافة معرفة جديدة
with st.expander("➕ إضافة معرفة جديدة"):
    with st.form("add_knowledge_form"):
        new_question = st.text_input("السؤال:")
        new_answer = st.text_area("الإجابة:")
        submit = st.form_submit_button("إضافة المعرفة")
        
        if submit and new_question and new_answer:
            if st.session_state.engine.add_knowledge(new_question, new_answer):
                st.success("✅ تم إضافة المعرفة بنجاح!")
                st.rerun()
            else:
                st.error("❌ فشل في إضافة المعرفة")

# تذييل الصفحة
st.markdown("---")
st.caption("🚀 نظام ذكاء اصطناعي محلي يعمل بدون إنترنت")
