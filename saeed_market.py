import os
import sys
import asyncio
import traceback
import io
import edge_tts
from PIL import Image
from google import genai
from google.genai import types

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
# 2. وظيفة التوليد الصوتي (التعليق الصوتي للرد)
# =====================================================================
async def speak_response(text, output_filename="response_audio.mp3"):
    try:
        voice = "ar-SA-ZariyahNeural"
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_filename)
    except Exception as e:
        print(f"Audio error: {e}")

def generate_audio_file(text):
    try:
        asyncio.run(speak_response(text))
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(speak_response(text))
    except Exception as e:
        print(f"Error generating audio: {e}")

# =====================================================================
# 3. دالة محرك الذكاء الموحد (نص + صور)
# =====================================================================
def get_gemini_smart_response(user_input):
    if not user_input or user_input.strip() == "":
        user_input = "مرحباً"

    api_key = get_api_key()
    if not api_key:
        return "⚠️ خطأ: لم يتم العثور على مفتاح GEMINI_MAIN_KEY!", None

    client = genai.Client(api_key=api_key)
    
    # 🎨 1. التحقق إذا كان الطلب يتضمن تصميم صورة
    image_keywords = ["صمم", "صورة", "ارسم", "توليد صورة", "إعلان مصور"]
    is_image_request = any(keyword in user_input for keyword in image_keywords)

    if is_image_request:
        try:
            # استخدام Imagen لتوليد الصور
            result = client.models.generate_images(
                model='imagen-3.0-generate-002',
                prompt=user_input,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    output_mime_type="image/jpeg",
                    aspect_ratio="1:1",
                )
            )
            for generated_image in result.generated_images:
                image = Image.open(io.BytesIO(generated_image.image.image_bytes))
                return "🖼️ تم تصميم الصورة بنجاح حسب طلبك!", image
        except Exception as e:
            print(f"Image generation failed: {e}")

    # 🛍️ 2. إذا كان الطلب نصوص/كوبونات/عروض
    system_instruction = """
أنت مساعد التسوق الذكي لـ Saeed MarketAds. 
وظيفتك الأساسية هي إعطاء كود الخصم فوراً ورابط العرض بشكل مباشر وواضح للمستخدم دون إعطاء نصائح عامة.

قائمة الأكواد والعروض المتاحة حالياً:
1. متجر SHEIN: كود الخصم (Saeed15) - خصم 15% على جميع المنتجات.
2. متجر نون (Noon): كود الخصم (SaeedNoon) - خصم إضافي وتوصيل مجاني.
3. متجر علي إكسبريس (AliExpress): كود الخصم (SaeedAE) - عروض مباشرة وتخفيض شحن.
"""

    try:
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.3,
            max_output_tokens=1024,
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_input,
            config=config,
        )
        reply_text = response.text.strip()
        
        # توليد الصوت للرد
        generate_audio_file(reply_text)
        
        return reply_text, None

    except Exception as e:
        return f"أهلاً بك. حدث خطأ أثناء التوليد: {e}", None
