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
# 1. إعداد مفتاح الربط مع Gemini (جلب آمن من Secrets أو Environment)
# =====================================================================
def get_api_key():
    # محاولة جلب المفتاح من Streamlit Secrets أولاً
    try:
        import streamlit as st
        if "GEMINI_MAIN_KEY" in st.secrets:
            return st.secrets["GEMINI_MAIN_KEY"]
        elif "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    
    # في حال التشغيل المحلي أو عدم وجود Streamlit Secrets
    return os.getenv("GEMINI_API_KEY", os.getenv("GEMINI_MAIN_KEY", ""))

GEMINI_API_KEY = get_api_key()
client = genai.Client(api_key=GEMINI_API_KEY)

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
        traceback.print_exc()

def generate_audio_file(text):
    try:
        asyncio.run(speak_response(text))
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(speak_response(text))
    except Exception as e:
        print(f"Error in generate_audio_file: {e}")

# =====================================================================
# 3. محرك الذكاء المرتبط بـ Gemini SDK
# =====================================================================
def get_gemini_smart_response(user_input):
    """
    ترسل أي نص يكتبه المستخدم مباشرة إلى خوارزميات Gemini الذكية،
    وتستقبل رداً متكاملاً، وتولد له ملفاً صوتياً فورياً.
    """
    if not user_input or user_input.strip() == "":
        user_input = "مرحباً"

    system_instruction = (
        "أنت مساعد التسوق الذكي لعلامة Saeed MarketAds. "
        "مهمتك مساعدة المستخدم في إدارة عروض التسوق والكوبونات وتوفير المال "
        "من منصات مثل AliExpress و Noon و SHEIN بطريقة ذكية، ودودة، ومحترفة باللغة العربية."
    )

    try:
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7,
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
        # طباعة الخطأ الكامل في سجلات السيرفر (Logs) لمعرفة السبب بدقة
        print("=== ERROR IN GEMINI GENERATION ===")
        traceback.print_exc()
        reply_text = f"أهلاً بك يا سعيد. عذراً واجهتني مشكلة بسيطة في الاتصال بالسيرفر ({e})، لكننا مستمرون تحت راية Saeed MarketAds!"

    # توليد الصوت للرد الناتج تلقائياً
    try:
        generate_audio_file(reply_text)
    except Exception as e:
        print(f"Audio generation skipped due to error: {e}")
    
    return reply_text

# =====================================================================
# 4. نقطة التشغيل الرئيسية للتجربة المحلية
# =====================================================================
if __name__ == "__main__":
    print("--- Saeed LogiC Pro (Gemini Powered Engine) is Online ---")
    
    test_query = "أعطيني نصيحة لتسويق منتجات نون اليوم"
    print(f"User Input: {test_query}")
    
    answer = get_gemini_smart_response(test_query)
    print(f"Gemini Response: {answer}")
