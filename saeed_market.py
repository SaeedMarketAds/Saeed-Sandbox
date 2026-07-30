import os
import sys
import asyncio
import traceback
import edge_tts
from google import genai
from google.genai import types

# =====================================================================
# 0. ضبط ترميز النظام لمنع أخطاء ASCII مع اللغة العربية
# =====================================================================
os.environ["PYTHONIOENCODING"] = "utf-8"
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# =====================================================================
# 1. دالة آمنة لجلب المفتاح
# =====================================================================
def get_api_key():
    try:
        import streamlit as st
        if "GEMINI_MAIN_KEY" in st.secrets and st.secrets["GEMINI_MAIN_KEY"]:
            return st.secrets["GEMINI_MAIN_KEY"]
        elif "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    
    return os.getenv("GEMINI_MAIN_KEY", os.getenv("GEMINI_API_KEY", ""))

# =====================================================================
# 2. وظيفة التوليد الصوتي (Neural Voice Synthesis)
# =====================================================================
async def speak_response(text, output_filename="response_audio.mp3"):
    try:
        voice = "ar-SA-ZariyahNeural"
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_filename)
    except Exception as e:
        print(f"Audio generation error: {e}")

def generate_audio_file(text):
    try:
        asyncio.run(speak_response(text))
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(speak_response(text))
    except Exception as e:
        print(f"Error in generate_audio_file: {e}")

# =====================================================================
# 3. محرك الذكاء المرتبط بـ Gemini SDK (آمن عند الاستيراد)
# =====================================================================
def get_gemini_smart_response(user_input):
    if not user_input or user_input.strip() == "":
        user_input = "مرحباً"

    api_key = get_api_key()
    if not api_key:
        return "⚠️ خطأ: لم يتم العثور على مفتاح GEMINI_MAIN_KEY في Streamlit Secrets!"

    system_instruction = """
أنت مساعد التسوق الذكي لـ Saeed MarketAds. 
وظيفتك الأساسية هي إعطاء كود الخصم فوراً ورابط العرض بشكل مباشر وواضح للمستخدم دون إعطاء نصائح عامة أو إجابات عائمة.

قائمة الأكواد والعروض المتاحة حالياً:
1. متجر SHEIN (شي إن):
   - كود الخصم: Saeed15
   - التفاصيل: خصم 15% على جميع المنتجات.
2. متجر نون (Noon):
   - كود الخصم: SaeedNoon
   - التفاصيل: خصم إضافي + توصيل مجاني.
3. متجر علي إكسبريس (AliExpress):
   - كود الخصم: SaeedAE
   - التفاصيل: عروض مباشرة وخصومات على الشحن.

عندما يطلب المستخدم كود خصم أو عرض لأي متجر:
- أعطه الكود فوراً وبخط بارز (Bold) ومباشر.
- اذكر نسبة الخصم والتفاصيل فوراً.
"""

    try:
        # إنشاء العميل داخل الدالة لضمان استيراد الملف بدون مشاكل
        client = genai.Client(api_key=api_key)
        
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.3,
            top_p=0.95,
            max_output_tokens=1024,
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_input,
            config=config,
        )
        reply_text = response.text.strip()

    except Exception as e:
        print("=== ERROR IN GEMINI GENERATION ===")
        traceback.print_exc()
        reply_text = f"أهلاً بك يا سعيد. عذراً واجهتني مشكلة أثناء الاتصال ({e})."

    # توليد الصوت تلقائياً
    try:
        generate_audio_file(reply_text)
    except Exception as e:
        print(f"Audio generation skipped: {e}")
    
    return reply_text
