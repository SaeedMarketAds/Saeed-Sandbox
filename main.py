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
def# =========================================================================
# 🎬 الموديل 4: المعلق وصانع الميديا الصوتي الفخم
# =========================================================================
def generate_promotional_audio(text_script: str):
    try:
        # استخدام عميل الصوت المستقل وتمرير أمر توليد الصوت AUDIO
        response = client_audio.models.generate_content(
            model='gemini-2.5-flash',  # استخدام الموديل الفلاشي السريع والداعم للصوت
            contents=f"اقرأ النص التالي بنبرة تسويقية حماسية وجذابة لمنصة تيك توك: {text_script}",
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"]  # إجبار المحرك على إرجاع صوت نقي
            )
        )
        
        # استخراج بايتات الصوت الذكية من رد المحرك
        audio_bytes = None
        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.mime_type.startswith("audio/"):
                audio_bytes = part.inline_data.data
                break
                
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3")
            st.success("🚀 تم توليد التعليق الصوتي بنجاح واحترافية!")
        else:
            st.warning("تم معالجة النص ولكن لم يتم إرجاع بايتات صوتية، تأكد من إعدادات الموديل.")
            
    except Exception as e:
        # التحويل التلقائي الذكي للمحرك الاحتياطي في حال حدوث أي ضغط
        st.warning("جاري محاولة التوليد عبر المحرك السحابي الاحتياطي...")
        try:
            client_backup = genai.Client(api_key=st.secrets["BACKUP_API_KEY"])
            response = client_backup.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"اقرأ النص التالي بنبرة تسويقية حماسية: {text_script}",
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"]
                )
            )
            
            audio_bytes = None
            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.mime_type.startswith("audio/"):
                    audio_bytes = part.inline_data.data
                    break
                    
            if audio_bytes:
                st.audio(audio_bytes, format="audio/mp3")
                st.success("🚀 تم الإنقاذ والتوليد عبر المحرك الاحتياطي بنجاح!")
        except Exception as backup_error:
            st.error(f"عذراً يا غالي، واجه وكيل الصوت مشكلة كاملة: {str(backup_error)}")

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
# 🔄 محرك التشغيل والربط التلقائي مع أزرار الوصول السريع
# =========================================================================

# 1. تهيئة متغير الإدخال السريع في الذاكرة
if "quick_action" not in st.session_state:
    st.session_state.quick_action = None

# 2. تصميم صف الأزرار الأفقية (يشبه حافظة ومختصرات لوحة المفاتيح)
st.markdown("<p style='text-align: right; margin-bottom: 5px; color: #888;'>⚡ اختصارات سريعة:</p>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📋 الحافظة (عروض اليوم)", use_container_width=True):
        st.session_state.quick_action = "استخرج لي أقوى كوبونات وعروض اليوم من قاعدة البيانات"

with col2:
    if st.button("🔥 جُمَلْ مُزْخْرَفَةٌ التسويقية", use_container_width=True):
        st.session_state.quick_action = "اكتب لي عبارة تسويقية مزخرفة وجذابة لمنتج عشوائي"

with col3:
    if st.button("🎙️ سكربت صوتي تيك توك", use_container_width=True):
        st.session_state.quick_action = "صمم لي سكربت إعلاني قصير مع تفعيل التعليق الصوتي"

# 3. استقبال النص سواء من الكتابة أو من ضغط الأزرار السريعة
chat_input_val = st.chat_input("اسأل Saeed LogiC عن العروض أو اطلب سكربت...")

# تحديد المدخل الفعلي
user_input = None
if chat_input_val:
    user_input = chat_input_val
elif st.session_state.quick_action:
    user_input = st.session_state.quick_action
    st.session_state.quick_action = None # تفريغ الذاكرة بعد الاستخدام

# 4. معالجة الطلب وبث النتيجة
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
            st.markdown("**[وكيل الميديا: Gemini الصوت]**")
            script_text = handle_general_chat(f"اكتب سكربت إعلاني قصير جداً وتكتوك حماسي بناءً على: {user_input}")
            st.write(script_text)
            generate_promotional_audio(script_text)
            
        else:
            st.markdown("**[مساعد الحوار: Gemini 3.5 Flash]**")
            reply = handle_general_chat(user_input)
            st.write(reply)


#

