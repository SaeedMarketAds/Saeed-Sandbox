import os
import asyncio
import edge_tts
from google import genai

# =====================================================================
# 1. إعداد مفتاح الربط مع Gemini
# =====================================================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSy_حط_مفتاحك_هنا_بدل_هذا_النص")

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

def generate_audio_file(text):
    try:
        asyncio.run(speak_response(text))
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(speak_response(text))

# =====================================================================
# 3. محرك الذكاء المرتبط بـ Gemini SDK الجديد
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
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=user_input,
            config={
                "system_instruction": system_instruction,
                "temperature": 0.7,
                "top_p": 0.95,
                "max_output_tokens": 1024,
            }
        )
        reply_text = response.text.strip()
    except Exception as e:
        reply_text = f"أهلاً بك يا سعيد. عذراً واجهتني مشكلة بسيطة في الاتصال بالسيرفر ({e})، لكننا مستمرون تحت راية Saeed MarketAds!"

    # توليد الصوت للرد الناتج تلقائياً
    generate_audio_file(reply_text)
    
    return reply_text

# =====================================================================
# 4. نقطة التشغيل الرئيسية
# =====================================================================
if __name__ == "__main__":
    print("--- Saeed LogiC Pro (Gemini Powered Engine) is Online ---")
    
    test_query = "أعطيني نصيحة لتسويق منتجات نون اليوم"
    print(f"User Input: {test_query}")
    
    answer = get_gemini_smart_response(test_query)
    print(f"Gemini Response: {answer}")
