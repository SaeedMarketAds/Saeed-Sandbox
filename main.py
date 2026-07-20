import json
import os
import streamlit as st
from google import genai
from google.genai import types

# 1. إعداد واجهة وتصميم التطبيق
st.set_page_config(page_title="Saeed LogiC Pro", page_icon="🚀", layout="centered")
st.title("Saeed LogiC Pro 🚀")
st.subheader("النظام التفاعلي الموحد لإدارة العروض والتسويق")

# 2. تهيئة عملاء الذكاء الاصطناعي بالمفاتيح الجديدة
try:
    # العميل الرئيسي (للبحث والفرز)
    client_main = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    # عميل الصوت المستقل (للتعليق الصوتي)
    client_audio = genai.Client(api_key=st.secrets["AUDIO_API_KEY"])
except Exception as e:
    st.error("❌ حدث خطأ في قراءة المفاتيح من صندوق الأسرار (Secrets)!")
    st.info("تأكد من كتابة GEMINI_API_KEY و AUDIO_API_KEY بشكل صحيح داخل الإعدادات.")
    st.stop()

# دالة مساعدة لقراءة قاعدة بيانات الكوبونات المحلية الخاصة بـ Saeed MarketAds
def load_local_coupons():
    try:
        with open("knowledge.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"error": f"حدث خطأ أثناء محاولة قراءة قاعدة المعرفة: {str(e)}"}

# =========================================================================
# 💻 الموديل 3: العقل الحواري العام والدعم الفني (Gemini 3.5 Flash)
# =========================================================================
def handle_general_chat(user_input: str) -> str:
    prompt = (
        f"أنت (Saeed LogiC Pro)، مساعد التسوق الذكي واللبق والمطور خصيصاً "
        f"لصالح منصة وشبكة (Saeed MarketAds) الرائدة في العروض والتسويق الرقمي.\n"
        f"أجب على العميل باختصار، وبلباقة ترحيبية عالية، واحترافية تامة. "
        f"تذكر دائماً هويتك كمساعد تسوق واعتزازك بكونك مدعوماً من Saeed MarketAds لإدارة أقوى الكوبونات.\n"
        f"الطلب: {user_input}"
    )
    response = client_main.models.generate_content(
        model='gemini-3.5-flash',
        contents=prompt
    )
    return response.text

    )
    return response.text.strip().lower()

# =========================================================================
# 🧠 الموديل 2: مهندس البيانات والمنطق البرمجي (Gemma 4 26B A4B IT)
# =========================================================================
def process_coupon_with_gemma(user_input: str) -> str:
    coupons_data = load_local_coupons()
    
    prompt = (
        f"أنت وكيل البيانات المسؤول عن قواعد عروض Saeed MarketAds. "
        f"بناءً على قاعدة البيانات المحلية التالية:\n{json.dumps(coupons_data, ensure_ascii=False)}\n"
        f"استخرج كود الخصم الدقيق وتفاصيله للرد على طلب العميل: {user_input}. "
        f"إذا لم تجد كوداً مناسباً، قل باختصار ولباقة: (لم أجد كوبوناً متاحاً لهذا الطلب حالياً)."
    )
    response = client_main.models.generate_content(
        model='gemma-4-26b-a4b-it',
        contents=prompt
    )
    return response.text

# =========================================================================
# 💻 الموديل 3: العقل الحواري العام والدعم الفني (Gemini 3.5 Flash)
# =========================================================================
def handle_general_chat(user_input: str) -> str:
    prompt = (
        f"أنت مساعد تسوق ذكي ولبق لتطبيق (Saeed LogiC Pro). "
        f"أجب على العميل باختصار وبلهجة ترحيبية وتذكر دائماً هويتك كمساعد تسوق. "
        f"الطلب: {user_input}"
    )
    response = client_main.models.generate_content(
        model='gemini-3.5-flash',
        contents=prompt
    )
    return response.text

# =========================================================================
# 🎬 الموديل 4: المعلق وصانع الميديا الصوتي (Gemini 3.1 Flash TTS Preview)
# =========================================================================
def generate_promotional_audio(text_script: str):
    try:
        # هنا نستخدم عميل الصوت المستقل AUDIO_API_KEY لتخفيف الضغط
        response = client_audio.models.generate_content(
            model='gemini-3.1-flash-tts-preview',
            contents=f"اقرأ النص التالي بنبرة تسويقية حماسية وجذابة لمنصة تيك توك: {text_script}"
        )
        if hasattr(response, 'audio_bytes') and response.audio_bytes:
            st.audio(response.audio_bytes, format="audio/mp3")
            st.success("🚀 تم توليد التعليق الصوتي بنجاح!")
        else:
            st.info("تمت معالجة النص بنجاح برمجياً.")
    except Exception as e:
        # إذا فشل المفتاح الثاني لأي سبب، نقوم بالتحويل الاحتياطي للمفتاح الثالث تلقائياً
        st.warning("جاري محاولة التوليد عبر المحرك الاحتياطي...")
        try:
            client_backup = genai.Client(api_key=st.secrets["BACKUP_API_KEY"])
            response = client_backup.models.generate_content(
                model='gemini-3.1-flash-tts-preview',
                contents=f"اقرأ النص التالي بنبرة تسويقية حماسية: {text_script}"
            )
            if hasattr(response, 'audio_bytes') and response.audio_bytes:
                st.audio(response.audio_bytes, format="audio/mp3")
        except Exception as backup_error:
            st.error(f"عذراً، واجه وكيل الصوت مشكلة: {str(backup_error)}")

# =========================================================================
# 🔄 محرك التشغيل والربط التلقائي
# =========================================================================
user_input = st.chat_input("...اسألني عن العروض أو اطلب سكربت تسويقي")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
        
    with st.spinner("جاري فحص وتوجيه طلبك برمجياً..."):
        selected_agent = route_user_request(user_input)
        
    with st.chat_message("assistant"):
        if "coupon" in selected_agent:
            st.markdown("**[وكيل البيانات: Gemma 4]**")
            reply = process_coupon_with_gemma(user_input)
            st.write(reply)
            
        elif "voice_script" in selected_agent:
            st.markdown("**[وكيل الميديا: Gemini 3.1 Flash TTS]**")
            script_text = handle_general_chat(f"اكتب سكربت إعلاني قصير جداً وتكتوك حماسي بناءً على: {user_input}")
            st.write(script_text)
            generate_promotional_audio(script_text)
            
        else:
            st.markdown("**[مساعد الحوار: Gemini 3.5 Flash]**")
            reply = handle_general_chat(user_input)
            st.write(reply)
