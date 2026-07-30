import sys
import os

# =====================================================================
# 1. ضبط الترميز الشامل ليدعم اللغة العربية بدون مشاكل ASCII
# =====================================================================
os.environ["PYTHONIOENCODING"] = "utf-8"
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

import streamlit as st
from saeed_market import get_gemini_smart_response

# =====================================================================
# 2. إعداد الصفحة والتصميم الرئيسي
# =====================================================================
st.set_page_config(
    page_title="Saeed LogiC Pro",
    page_icon="🛍️",
    layout="centered"
)

st.title("🛍️ Saeed LogiC Pro - مساعد التسوق والتصميم الذكي")
st.caption("المحرك الذكي لعلامة Saeed MarketAds")
st.markdown("---")
st.markdown("💡 **مرحباً بك يا سعيد!** اكتب استفسارك عن العروض، أو اطلب تصميم صورة/إعلان لمشروعك.")

# =====================================================================
# 3. إدارة ذاكرة الجلسة (Session State)
# =====================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================================================
# 4. عرض المحادثات السابقة (نصوص + صور محفوظة)
# =====================================================================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # عرض الصورة المرفقة إذا كانت مسبقاً في سجل هذه الرسالة
        if message.get("image") is not None:
            st.image(message["image"], caption="تصميم SaeedMarketAds 🛍️", use_container_width=True)

# =====================================================================
# 5. استقبال مدخلات المستخدم ومعالجتها
# =====================================================================
if user_input := st.chat_input("اكتب سؤالك أو طلب التصميم هنا (مثلاً: عروض نون اليوم أو صمم صورة إعلان)..."):
    
    # 1) إضافة وتجسيد رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": user_input, "image": None})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2) معالجة وتوليد الرد الذكي (نص + صورة + صوت)
    with st.chat_message("assistant"):
        with st.spinner("جاري معالجة الطلب وتجهيز الرد والتصميم..."):
            
            # استدعام المحرك الذكي من saeed_market.py
            bot_reply, generated_img = get_gemini_smart_response(user_input)
            
            # أ) عرض النص
            st.markdown(bot_reply)
            
            # ب) عرض الصورة إن تم توليدها
            if generated_img is not None:
                st.image(generated_img, caption="تم التصميم بواسطة SaeedMarketAds 🛍️", use_container_width=True)
            
            # ج) تشغيل مشغل الصوت للرد النصي
            if os.path.exists("response_audio.mp3"):
                try:
                    with open("response_audio.mp3", "rb") as f:
                        audio_bytes = f.read()
                        st.audio(audio_bytes, format="audio/mp3")
                except Exception as e:
                    print(f"Error reading audio file: {e}")

            # 3) حفظ الرد النصي والصورة في سجل المحادثة
            st.session_state.messages.append({
                "role": "assistant", 
                "content": bot_reply, 
                "image": generated_img
            })
