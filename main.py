import streamlit as st
import os

# 1. إنشاء المجلدات مباشرة (بدون دالة لتفادي أي خطأ NameError نهائياً)
os.makedirs("data", exist_ok=True)
os.makedirs("memory", exist_ok=True)

# 2. محاولة استيراد محرك الذكاء الاصطناعي
try:
    from inference import InferenceEngine
except ImportError as e:
    st.error(f"🚨 خطأ في استيراد ملف التشغيل: {e}")
    st.info("تأكد من وجود الملفات باسم app_utils.py و inference.py في حسابك.")
    st.stop()

# تهيئة واجهة التطبيق
st.set_page_config(page_title="Saeed Sandbox", page_icon="🤖", layout="centered")

st.title("🤖 سعيد سانـدبوكس | SaeeD SanDboX")
st.write("---")

# تشغيل محرك الذكاء الاصطناعي وحفظه في الذاكرة المؤقتة
@st.cache_resource
def load_engine():
    try:
        return InferenceEngine()
    except Exception as e:
        st.error(f"❌ حدث خطأ أثناء تشغيل محرك الذكاء الاصطناعي: {e}")
        return None

engine = load_engine()

if engine is not None:
    # تهيئة سجل المحادثات
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض الرسائل السابقة للمستخدم
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # استقبال سؤال المستخدم الجديد
    user_input = st.chat_input("اكتب سؤالك هنا...")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.spinner("جاري التفكير... ⏳"):
            response = engine.answer(user_input)
            
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.warning("⚠️ يرجى إصلاح الأخطاء المذكورة أعلاه ليتمكن المحرك من العمل.")
