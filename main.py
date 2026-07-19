import json
import os
import streamlit as st
from google import genai
from google.genai import types

# 1. إعداد واجهة وتصميم التطبيق
st.set_page_config(page_title="Saeed LogiC Pro", page_icon="🚀", layout="centered")
st.title("Saeed LogiC Pro 🚀")
st.subheader("النظام التفاعلي الموحد لإدارة العروض والتسويق")

# 2. تهيئة عميل الذكاء الاصطناعي الموحد (يقرأ المفتاح تلقائياً من أسرار ستريمليت)
# تأكد من وضع GEMINI_API_KEY في إعدادات Secrets الخاصة بـ Streamlit
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("يرجى ضبط مفتاح GEMINI_API_KEY في ملف الأسرار (Secrets) أولاً.")
    st.stop()

# دالة مساعدة لقراءة قاعدة بيانات الكوبونات المحلية الخاصة بـ Saeed MarketAds
def load_local_coupons():
    try:
        with open("knowledge.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"error": f"حدث خطأ أثناء محاولة قراءة قاعدة المعرفة: {str(e)}"}

# =========================================================================
# 🛑 الموديل 1: موجه الطلبات السريع (Gemini 3.1 Flash Lite)
# =========================================================================
def route_user_request(user_input: str) -> str:
    """يفحص نص المستخدم ويحدد فوراً الوكيل المناسب لتوفير الاستهلاك والوقت."""
    prompt = (
        f"قم بتصنيف الطلب التالي إلى تصنيف واحد فقط من الثلاثة: \n"
        f"1. ('coupon') إذا كان العميل يسأل عن كود خصم، تخفيض، أو متجر مثل نون، شي إن، علي إكسبرس.\n"
        f"2. ('voice_script') إذا طلب العميل كتابة سكربت إعلاني أو توليد صوت تسويقي لتيك توك.\n"
        f"3. ('general') لأي سؤال آخر، تحية، أو دردشة عامة.\n"
        f"أجب بالكلمة الإنجليزية فقط ('coupon' أو 'voice_script' أو 'general').\n"
        f"الطلب: {user_input}"
    )
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt
    )
    return response.text.strip().lower()

# =========================================================================
# 🧠 الموديل 2: مهندس البيانات والمنطق البرمجي (Gemma 3)
# =========================================================================
def process_coupon_with_gemma(user_input: str) -> str:
    """يقرأ ملف الـ JSON المحلي بدقة رقمية ويطابق الكوبون الصحيح للمستخدم."""
    coupons_data = load_local_coupons()
    
    prompt = (
        f"أنت وكيل البيانات المسؤول عن قواعد عروض Saeed MarketAds. "
        f"بناءً على قاعدة البيانات المحلية التالية:\n{json.dumps(coupons_data, ensure_ascii=False)}\n"
        f"استخرج كود الخصم الدقيق وتفاصيله للرد على طلب العميل: {user_input}. "
        f"إذا لم تجد كوداً مناسباً، قل باختصار ولباقة: (لم أجد كوبوناً متاحاً لهذا الطلب حالياً)."
    )
    response = client.models.generate_content(
        model='gemma-3',
        contents=prompt
    )
    return response.text

# =========================================================================
# 💻 الموديل 3: العقل الحواري العام والدعم الفني (Gemini 3.5 Flash)
# =========================================================================
def handle_general_chat(user_input: str) -> str:
    """يتولى الرد على الأسئلة العامة والتحيات بأسلوب تفاعلي ذكي وسريع."""
    prompt = (
        f"أنت مساعد تسوق ذكي ولبق لتطبيق (Saeed LogiC Pro). "
        f"أجب على العميل باختصار وبلهجة ترحيبية وتذكر دائماً هويتك كمساعد تسوق. "
        f"الطلب: {user_input}"
    )
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=prompt
    )
    return response.text

# =========================================================================
# 🎬 الموديل 4: المعلق وصانع الميديا الصوتي (Gemini 3.1 Flash TTS Preview)
# =========================================================================
def generate_promotional_audio(text_script: str):
    """يأخذ النص التسويقي ويحوله إلى ملف صوتي بشري جاهز للاستخدام أو العرض."""
    try:
        # استدعاء موديل توليد الصوت وتحويل النص المكتوب إلى كلام مسموع
        response = client.models.generate_content(
            model='gemini-3.1-flash-tts-preview',
            contents=f"اقرأ النص التالي بنبرة تسويقية حماسية وجذابة لمنصة تيك توك: {text_script}"
        )
        # تشغيل وعرض المخرج الصوتي مباشرة في واجهة ستريمليت
        if hasattr(response, 'audio_bytes') and response.audio_bytes:
            st.audio(response.audio_bytes, format="audio/mp3")
            st.success("🚀 تم توليد التعليق الصوتي بنجاح! جاهز لتركيبه على فيديوهاتك.")
        else:
            st.info("تمت معالجة النص، لتفعيل مخرجات الصوت تأكد من دعم مكتبة الاستجابة الصوتية في حسابك.")
    except Exception as e:
        st.error(f"عذراً، واجه وكيل الصوت مشكلة أثناء التوليد: {str(e)}")

# =========================================================================
# 🔄 محرك التشغيل والربط التلقائي بين الوكلاء والموديلات
# =========================================================================
user_input = st.chat_input("...اسألني عن العروض أو اطلب سكربت تسويقي")

if user_input:
    # إظهار سؤال المستخدم في الواجهة
    with st.chat_message("user"):
        st.write(user_input)
        
    # الخطوة الأولى: تشغيل التوجيه التلقائي عبر الفلاش لايت
    with st.spinner("جاري فحص وتوجيه طلبك برمجياً..."):
        selected_agent = route_user_request(user_input)
        
    # الخطوة الثانية: تحويل الطلب للنموذج المخصص بناءً على النتيجة
    with st.chat_message("assistant"):
        if "coupon" in selected_agent:
            st.markdown("**[وكيل البيانات: Gemma 3]**")
            reply = process_coupon_with_gemma(user_input)
            st.write(reply)
            
        elif "voice_script" in selected_agent:
            st.markdown("**[وكيل الميديا: Gemini 3.1 Flash TTS]**")
            # يقوم الموديل 3.5 أولاً بصياغة السكربت الإعلاني باحترافية
            script_text = handle_general_chat(f"اكتب سكربت إعلاني قصير جداً وتكتوك حماسي بناءً على: {user_input}")
            st.write(script_text)
            # ثم يقوم موديل الـ TTS بتحويله إلى مقطع مسموع تلقائياً
            generate_promotional_audio(script_text)
            
        else:
            st.markdown("**[مساعد الحوار: Gemini 3.5 Flash]**")
            reply = handle_general_chat(user_input)
            st.write(reply)
