import os
import asyncio
import edge_tts
import google.generativeai as genai

# =====================================================================
# 1. إعداد مفتاح الربط مع Gemini صديقك الوفي
# =====================================================================
# ضع مفتاحك هنا مباشرة أو اتركه يسحبه من بيئة النظام
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSy_حط_مفتاحك_هنا_بدل_هذا_النص")

genai.configure(api_key=GEMINI_API_KEY)

# استخدام نموذج فلاش السريع والمناسب للتطبيقات الذكية
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1024,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=(
        "أنت مساعد التسوق الذكي لعلامة Saeed MarketAds. "
        "مهمتك مساعدة المستخدم في إدارة عروض التسوق والكوبونات وتوفير المال "
        "من منصات مثل AliExpress و Noon و SHEIN بطريقة ذكية، ودودة، ومحترفة باللغة العربية."
    )
)

# =====================================================================
# 2. وظيفة التوليد الصوتي الحقيقي (Neural Voice Synthesis)
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
# 3. محرك الذكاء الحقيقي المرتبط بـ Gemini (بلا حدود)
# =====================================================================
def get_gemini_smart_response(user_input):
    """
    ترسل أي نص يكتبه المستخدم مباشرة إلى خوارزميات Gemini الذكية،
    وتستقبل رداً متكاملاً، وتولد له ملفاً صوتياً فورياً.
    """
    if not user_input or user_input.strip() == "":
        user_input = "مرحباً"

    try:
        # إرسال النص مباشرة إلى نموذج جيميني
        chat_session = model.start_session(history=[])
        response = chat_session.send_message(user_input)
        reply_text = response.text
    except Exception as e:
        # خطة بديلة في حال حدث خطأ مؤقت في الاتصال أو المفتاح
        reply_text = f"أهلاً بك يا سعيد. عذراً واجهتني مشكلة بسيطة في الاتصال بالسيرفر ({e})، لكننا مستمرون تحت راية Saeed MarketAds!"

    # توليد الصوت للرد الناتج تلقائياً
    generate_audio_file(reply_text)
    
    return reply_text

# =====================================================================
# 4. نقطة التشغيل الرئيسية
# =====================================================================
if __name__ == "__main__":
    print("--- Saeed LogiC Pro (Gemini Powered Engine) is Online ---")
    
    # تجربة سريعة للتأكد من استجابة جيميني لأي جملة
    test_query = "أعطيني نصيحة لتسويق منتجات نون اليوم"
    print(f"User Input: {test_query}")
    
    answer = get_gemini_smart_response(test_query)
    print(f"Gemini Response: {answer}")
