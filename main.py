import json
import os
import re
import asyncio
import streamlit as st
from google import genai
from google.genai import types
import edge_tts
import edge_tts

# --- دالة تجهيز وتنظيف النص للنطق الصوتي ---
import re

def prepare_text_for_speech(text: str) -> str:
    replacements = [
        # 1. ضبط لفظ الجلالة (الله) بالتشكيل الصحيح حتى ينطقه القارئ بفصاحة
        (r'\bورحمة الله\b', 'وَرَحْمَةُ اللَّهِ'),
        (r'\bالله\b', 'اللَّهِ'),
        
        # 2. حذف كلمة "يا فندم" و "فندم" تماماً من الصوت
        (r'\bيا\s+فندم\b', ''),
        (r'\bفندم\b', ''),
        
        # 3. ضبط المصطلحات والأسماء بالتشكيل الصحيح
        (r'\bSaeed\s+LogiC\s+Pro\b', 'سَعِيد لُوجِيك بْرُو'),
        (r'\bSaeed\s+Logic\s+Pro\b', 'سَعِيد لُوجِيك بْرُو'),
        (r'\bSaeed\s+LogiC\b', 'سَعِيد لُوجِيك'),
        (r'\bSaeed\s+Logic\b', 'سَعِيد لُوجِيك'),
        (r'\bSaeed\s+MarketAds\b', 'سَعِيد مَارْكِت أَدْس'),
        (r'\bSaeed\b', 'سَعِيد'),
        (r'\bMarketAds\b', 'مَارْكِت أَدْس'),
        (r'\bPro\b', 'بْرُو'),
        (r'\bSHEIN\b', 'شِي إن'),
        (r'\bAliExpress\b', 'عَلِي إكْسِبْرِيس'),
        (r'\bNoon\b', 'نُون'),
        (r'\bSAED\b', 'سَعِيد'),
        
        # 4. ضبط الكلمات العربية
        (r'\bأهلاً\b', 'أَهْلًا'),
        (r'\bاهلاً\b', 'أَهْلًا'),
    ]

    # تطبيق التبديل بغض النظر عن حالة الأحرف
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    # إزالة الرموز والأقواس وتنظيف المسافات
    text = re.sub(r'[*#_~`>\[\]\(\)]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text


# 1. إعداد واجهة وتصميم التطبيق

# 1. إعداد واجهة وتصميم التطبيق
st.set_page_config(page_title="Saeed LogiC Pro", page_icon="🚀", layout="centered")
st.title("Saeed LogiC Pro 🚀")
st.subheader("النظام التفاعلي الموحد لإدارة العروض والتسويق")

# 2. تهيئة عملاء الذكاء الاصطناعي بالمفاتيح
try:
    client_main = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    client_audio = genai.Client(api_key=st.secrets["AUDIO_API_KEY"])
except Exception as e:
    st.error("❌ حدث خطأ في قراءة المفاتيح من صندوق الأسرار (Secrets)!")
    st.info("تأكد من كتابة GEMINI_API_KEY و AUDIO_API_KEY بشكل صحيح داخل الإعدادات.")
    st.stop()

# 3. دالة قراءة قاعدة البيانات المحلية
def load_local_coupons():
    try:
        with open("knowledge.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"error": f"حدث خطأ أثناء محاولة قراءة قاعدة المعرفة: {str(e)}"}

# 4. الموديل 1: العقل الحواري العام والدعم الفني (Gemini 3.5 Flash)
def handle_general_chat(user_input: str) -> str:
    prompt = (
        f"أنت (Saeed LogiC Pro)، مساعد التسوق الذكي واللبق والمطور خصيصاً "
        f"لصالح منصة وشبكة (Saeed MarketAds) الرائدة في العروض والتسويق الرقمي.\n"
        f"أجب على العميل باختصار، وبلباقة ترحيبية عالية، واحترافية تامة. "
        f"تذكر دائماً هويتك كمساعد تسوق واعتزازك بكونك مدعوماً من Saeed MarketAds لإدارة أقوى الكوبونات.\n"
        f"الطلب: {user_input}"
    )
    def handle_general_chat(user_input: str) -> str:
    try:
        response = client_main.models.generate_content(
            model="gemini-2.5-flash",  # استخدم اسم موديل معتمد ورسمي
            contents=user_input
        )
        return response.text
    except Exception as e:
        # إرجاع نص عربي بدلاً من انهيار التطبيق بالشاشة الحمراء
        return f"عذراً، تعذر الاتصال بمساعد الحوار حالياً. التفاصيل: {str(e)}"


# 5. الموديل 2: مهندس البيانات والمنطق البرمجي (Gemma 4 26B)
def process_coupon_with_gemma(user_input: str) -> str:
    coupons_data = load_local_coupons()
    prompt = (
        f"أنت وكيل البيانات المسؤول عن قواعد عروض Saeed MarketAds.\n"
        f"بناءً على قاعدة البيانات المحلية التالية:\n{json.dumps(coupons_data, ensure_ascii=False)}\n"
        f"استخرج كود الخصم الدقيق وتفاصيله للرد على طلب العميل: {user_input}.\n"
        f"إذا لم تجد كوداً مناسباً، قل باختصار ولباقة: (لم أجد كوبوناً متاحاً لهذا الطلب حالياً)."
    )
    response = client_main.models.generate_content(
        model='gemma-4-26b-a4b-it',
        contents=prompt
    )
    return response.text.strip()

# 6. صانع التعليق الصوتي الواقعي وتنظيف النصوص
def clean_text_for_speech(text: str) -> str:
    # إزالة كافة النجوم ورموز التنسيق (Markdown)
    text = re.sub(r'\*+', '', text)
    # إزالة التوجيهات البصرية بين أقواس مثل [المشهد البصري] أو [0:12]
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\(.*?\)', '', text)
    # إزالة الهاشتاجات والرموز الزائدة
    text = re.sub(r'#+', '', text)
    return text.strip()

async def _text_to_speech_async(text: str, output_path: str):
    voice = "ar-SA-HamedNeural"
    clean_text = clean_text_for_speech(text)
    communicate = edge_tts.Communicate(clean_text, voice)
    await communicate.save(output_path)

def generate_promotional_audio(text_script: str):
    try:
        audio_file_path = "promo_voice.mp3"
        asyncio.run(_text_to_speech_async(text_script, audio_file_path))

        with open(audio_file_path, "rb") as f:
            st.audio(f.read(), format="audio/mp3")

        st.success("تم توليد التعليق الصوتي الواقعي بنجاح! 🎙")
    except Exception as e:
        st.error(f"عذراً يا غالي، واجه وكيل الصوت مشكلة: {str(e)}")

# 7. توجيه الطلبات
def route_user_request(user_input: str) -> str:
    lowered = user_input.lower()
    if any(w in lowered for w in ["كوبون", "خصم", "كود", "عروض", "عرض"]):
        return "coupon"
    elif any(w in lowered for w in ["صوت", "سكربت", "تيك توك", "إعلان"]):
        return "voice_script"
    return "general"

# 8. واجهة المستخدم والتفاعل
if "quick_action" not in st.session_state:
    st.session_state.quick_action = None

st.markdown("<p style='text-align: right; margin-bottom: 5px; color: #888;'>⚡ اختصارات سريعة:</p>", unsafe_allow_html=True)
import json

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📋 العروض الكبرى", use_container_width=True, key="btn_main_offers"):
        try:
            with open("data/knowledge.json", "r", encoding="utf-8") as f:
                knowledge_data = json.load(f)
            
            coupons = knowledge_data.get("coupons", [])
            if coupons:
                st.success("🎉 إليك أحدث العروض والكوبونات المتاحة:")
                for item in coupons:
                    st.markdown(f"### 🏷️ {item.get('store')}")
                    st.code(item.get('code'), language="text")
                    st.write(f"**الوصف:** {item.get('description')}")
                    st.divider()
            else:
                st.warning("لا توجد عروض مسجلة حالياً.")
        except Exception as e:
            st.error(f"تعذر قراءة قاعدة البيانات: {e}")

with col2:
    if st.button("🔥 جملة تسويقية", use_container_width=True, key="btn_main_marketing"):
        st.info("💡 اختر المتجر المطلوب للحصول على النص التسويقي المخصص.")

with col3:
    if st.button("🎙️ سكريبت صوتي", use_container_width=True, key="btn_main_script"):
        st.info("🎙️ جاهز لتوليد السكريبت الصوتي للترويج للعروض.")

chat_input_val = st.chat_input("اسأل Saeed LogiC عن العروض أو اطلب سكربت...")

user_input = None
if chat_input_val:
    user_input = chat_input_val
elif st.session_state.quick_action:
    user_input = st.session_state.quick_action
    st.session_state.quick_action = None

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
            st.markdown("**[وكيل الصوت: Gemini الصوت]**")
            raw_script = handle_general_chat(f"اكتب سكريبت إعلاني قصير جداً وتنسيقي حماسي بناءً على: {user_input}")
            
            # 1. تجهيز النص العربي الفصيح وتعديل الأسماء قبل النطق
            speech_text = prepare_text_for_speech(raw_script)
            st.write(raw_script)
            
            # 2. توليد الصوت بالنص المجهز والمنظف
            generate_promotional_audio(speech_text)
        else:
            st.markdown("**[مساعد الحوار: Gemini 3.5 Flash]**")
            reply = handle_general_chat(user_input)
            st.write(reply)
            generate_promotional_audio(prepare_text_for_speech(reply))
