import sys
import os

# ضبط الترميز ليدعم اللغة العربية بدقة وبدون أخطاء ASCII
os.environ["PYTHONIOENCODING"] = "utf-8"
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

import streamlit as st
from saeed_market import get_gemini_smart_response, generate_audio_file

# إعداد الصفحة وتصميم المتصفح
st.set_page_config(
    page_title="Saeed LogiC Pro",
    page_icon="🛍️",
    layout="centered"
)

st.title("🛍️ Saeed LogiC Pro - مساعد التسوق الذكي")
st.markdown("---")
st.markdown("💡 **مرحباً بك يا سعيد!** اكتب استفسارك عن المنتجات أو العروض وسأقوم بمساعدتك فوراً.")

# إدارة تاريخ المحادثة في الذاكرة المؤقتة للجلسة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال مدخلات المستخدم عبر مربع الدردشة
if user_input := st.chat_input("اكتب سؤالك هنا (مثلاً: عروض نون اليوم)..."):
    # عرض رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # توليد رد الذكاء الاصطناعي عبر موديل model="gemini-3.1-flash",
    with st.chat_message("assistant"):
        with st.spinner("جاري البحث عن أفضل العروض وتجهيز الرد..."):
            bot_reply = get_gemini_smart_response(user_input)
            st.markdown(bot_reply)
            
            # حفظ الرد في التاريخ
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            
            # توليد التشغيل الصوتي (اختياري)
            try:
                generate_audio_file(bot_reply)
                if os.path.exists("response_audio.mp3"):
                    with open("response_audio.mp3", "rb") as audio_file:
                        audio_bytes = audio_file.read()
                        st.audio(audio_bytes, format="audio/mp3")
            except Exception:
                pass
