import streamlit as st
from rich.markdown import Markdown
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

# إدارة تاريخ المحادثة في الذاكرة المؤقتة للسيشن
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال مدخلات المستخدم عبر مربع الدردشة المرئي
if user_input := st.chat_input("اكتب سؤالك هنا (مثلاً: عروض نون اليوم)..."):
    # عرض رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # توليد رد الذكاء الاصطناعي
    with st.chat_message("assistant"):
        with st.spinner("جاري البحث عن أفضل العروض وتجهيز الرد..."):
            bot_reply = get_gemini_smart_response(user_input)
            st.markdown(bot_reply)
            
            # حفظ الرد في التاريخ
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            
            # توليد الملف الصوتي (اختياري للويب)
            try:
                generate_audio_file(bot_reply)
                with open("response_audio.mp3", "rb") as audio_file:
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format="audio/mp3")
            except Exception:
                pass
