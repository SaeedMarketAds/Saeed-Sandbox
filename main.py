import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)

import json
import os
import re
import io
import time
import asyncio
import requests
import streamlit as st
from PIL import Image
from google import genai
from google.genai import types
import edge_tts

import edge_tts
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

# --- دالة ضبط النص العربي ---
def fix_arabic(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

# --- دالة إنشاء تصميم Gemini الاحترافي ---
# --- دالة إنشاء تصميم Gemini الاحترافي ---
def create_gemini_style_arabic_design():
    W, H = 1080, 1920
    base = Image.new("RGBA", (W, H), (15, 23, 42, 255))
    
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    glow_draw.ellipse([50, 100, 750, 800], fill=(99, 102, 241, 150))
    glow_draw.ellipse([600, 1200, 1150, 1750], fill=(236, 72, 153, 130))
    glow_draw.ellipse([W//2 - 250, H//2 - 250, W//2 + 250, H//2 + 250], fill=(14, 165, 233, 90))
    
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(100))
    base = Image.alpha_composite(base, glow_layer)
    
    card_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    card_draw = ImageDraw.Draw(card_layer)
    card_rect = [80, 200, 1000, 1720]
    card_draw.rounded_rectangle(card_rect, radius=40, fill=(255, 255, 255, 20), outline=(255, 255, 255, 55), width=3)
    base = Image.alpha_composite(base, card_layer)
    
    try:
        title_font = ImageFont.truetype("Cairo-Bold.ttf", 60)
        sub_font = ImageFont.truetype("Cairo-Regular.ttf", 32)
        badge_font = ImageFont.truetype("Cairo-Bold.ttf", 24)
        button_font = ImageFont.truetype("Cairo-Bold.ttf", 36)
    except OSError:
        title_font = sub_font = badge_font = button_font = ImageFont.load_default()

    try:
        product_img = Image.open("product.png").convert("RGBA")
        product_img = product_img.resize((500, 500))
        base.paste(product_img, ((W - 500) // 2, 550), product_img)
    except FileNotFoundError:
        pass

    draw = ImageDraw.Draw(base)
    right_x = 940
    
    # تمت إزالة direction='rtl' لضمان التوافق التام مع Streamlit Cloud
    badge_text = fix_arabic("إصدار محدود 2026")
    draw.rounded_rectangle([right_x - 220, 260, right_x, 310], radius=12, fill=(99, 102, 241, 230))
    draw.text((right_x - 200, 272), badge_text, font=badge_font, fill="white")
    
    draw.text((right_x - 550, 360), fix_arabic("سماعات الذكاء الاصطناعي"), font=title_font, fill="white")
    draw.text((right_x - 620, 460), fix_arabic("تجربة صوتية ثورية تدمج الفن بالتكنولوجيا"), font=sub_font, fill=(226, 232, 240))
    
    btn_w = 300
    btn_rect = [(W - btn_w) // 2, 1150, (W + btn_w) // 2, 1230]
    draw.rounded_rectangle(btn_rect, radius=20, fill=(236, 72, 153, 255))
    draw.text((btn_rect[0] + 65, 1168), fix_arabic("اطلب الآن"), font=button_font, fill="white")
    
    return base.convert("RGB")


# استدعاء تصميم Gemini الاحترافي
img = create_gemini_style_arabic_design()

# =========================================================
# مفاتيح وإعدادات نموذج سعيد لوجيك (Saeed LogiC)
# =========================================================

MODEL_NAME = "gemini-2.5-flash"
IMAGEN_MODEL_NAME = "imagen-3.0-generate-002"
VEO_MODEL_NAME = "veo-2.0-generate-001"

# قراءة المفاتيح من Streamlit Secrets
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
AUDIO_API_KEY = st.secrets.get("AUDIO_API_KEY", "")
BACKUP_API_KEY = st.secrets.get("BACKUP_API_KEY", "")
IMAGEN_API_KEY = st.secrets.get("IMAGEN_API_KEY", "")

# تهيئة العملاء الرسميين
active_key = GEMINI_API_KEY or BACKUP_API_KEY
client_main = genai.Client(api_key=active_key)
client_audio = genai.Client(api_key=AUDIO_API_KEY or active_key)
client_imagen = genai.Client(api_key=IMAGEN_API_KEY or active_key)



# --- دالة تجهيز وتنظيف النص للنطق الصوتي ---
def prepare_text_for_speech(text: str) -> str:
    replacements = [
        # 1. ضبط لفظ الجلالة (الله) بالتشكيل الصحيح
        (r'\bورحمة الله\b', 'وَرَحْمَةُ اللَّهِ'),
        (r'\bالله\b', 'اللَّهِ'),
        
        # 2. حذف كلمة "يا فندم" و "فندم"
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
        (r'\bأهلاً\b', 'أَهْلًا'),
        (r'\bاهلاً\b', 'أَهْلًا'),
    ]

    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    text = re.sub(r'[*#_~`>\[\]\(\)]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def clean_text_for_speech(text: str) -> str:
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\(.*?\)', '', text)
    text = re.sub(r'#+', '', text)
    return text.strip()


# =========================================================
# 1. إعداد واجهة وتصميم التطبيق
# =========================================================
st.set_page_config(page_title="Saeed LogiC Pro", page_icon="🚀", layout="centered")
st.title("Saeed LogiC Pro 🚀")
st.subheader("النظام التفاعلي الموحد لإدارة العروض والصوت والصور والفيديو والموسيقى")


# =========================================================
# 2. دالة قراءة قاعدة البيانات المحلية
# =========================================================
def load_local_coupons():
    file_paths = ["knowledge.json", "data/knowledge.json"]
    for path in file_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                return {"error": f"حدث خطأ أثناء محاولة قراءة قاعدة المعرفة: {str(e)}"}
    return {"error": "لم يتم العثور على ملف قاعدة المعرفة knowledge.json"}


# =========================================================
# 3. الموديل 1: العقل الحواري العام والدعم الفني
# =========================================================
def handle_general_chat(user_input: str) -> str:
    prompt = (
        f"أنت (Saeed LogiC Pro)، مساعد التسوق الذكي واللبق والمطور خصيصاً "
        f"لصالح منصة وشبكة (Saeed MarketAds) الرائدة في العروض والتسويق الرقمي.\n"
        f"أجب على العميل باختصار، وبلباقة ترحيبية عالية، واحترافية تامة. "
        f"تذكر دائماً هويتك كمساعد تسوق واعتزازك بكونك مدعوماً من Saeed MarketAds لإدارة أقوى الكوبونات.\n"
        f"الطلب: {user_input}"
    )
    try:
        response = client_main.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"عذراً، تعذر الاتصال بمساعد الحوار حالياً. التفاصيل: {str(e)}"


# =========================================================
# 4. الموديل 2: مهندس البيانات والمنطق البرمجي (Gemma)
# =========================================================
def process_coupon_with_gemma(user_input: str) -> str:
    coupons_data = load_local_coupons()
    prompt = (
        f"أنت وكيل البيانات المسؤول عن قواعد عروض Saeed MarketAds.\n"
        f"بناءً على قاعدة البيانات المحلية التالية:\n{json.dumps(coupons_data, ensure_ascii=False)}\n"
        f"استخرج كود الخصم الدقيق وتفاصيله للرد على طلب العميل: {user_input}.\n"
        f"إذا لم تجد كوداً مناسباً، قل باختصار ولباقة: (لم أجد كوبوناً متاحاً لهذا الطلب حالياً)."
    )
    try:
        response = client_main.models.generate_content(
            model='gemma-4-26b-a4b-it',
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"عذراً، تعذر جلب معلومات الكوبون. التفاصيل: {str(e)}"


# =========================================================
# 5. صانع التعليق الصوتي والموسيقى
# =========================================================
async def _text_to_speech_async(text: str, output_path: str):
    voice = "ar-SA-HamedNeural"
    clean_text = clean_text_for_speech(text)
    communicate = edge_tts.Communicate(clean_text, voice)
    await communicate.save(output_path)

def generate_promotional_audio(text_script: str, output_path: str = "promo_voice.mp3") -> str:
    try:
        asyncio.run(_text_to_speech_async(text_script, output_path))
        with open(output_path, "rb") as f:
            st.audio(f.read(), format="audio/mp3")
        st.success("تم توليد التعليق الصوتي بنجاح! 🎙")
        return output_path
    except Exception as e:
        st.error(f"عذراً يا غالي، واجه وكيل الصوت مشكلة: {str(e)}")
        return None


# =========================================================
# 6. دالة توليد الصور الآمنة باستخدام Imagen
# =========================================================
def generate_image(prompt):
    try:
        # استخدام client_imagen بدلاً من client لأنه المتغير الذي عرفته في الأعلى
        response = client_imagen.models.generate_images(
            model=IMAGEN_MODEL_NAME,
            prompt=prompt,
            config=dict(
                number_of_images=1,
                output_mime_type="image/jpeg",
                aspect_ratio="1:1"
            )
        )
        # حفظ الصورة الموَلّدة
        for generated_image in response.generated_images:
            image_path = "generated_output.png"
            image = Image.open(io.BytesIO(generated_image.image.image_bytes))
            image.save(image_path)
            return image_path
            
    except Exception as e:
        st.error(f"عذراً! حدث خطأ أثناء توليد الصورة: {str(e)}")
        return None


# =========================================================
# 7. وكيل توليد الموسيقى والألحان
# =========================================================
def generate_music_track(prompt_text: str, output_path: str = "promo_music.mp3") -> str:
    try:
        st.info("🎵 جاري إنشاء الموسيقى والنغمة التسويقية...")
        music_description = handle_general_chat(f"وصف موسيقي تسويقي حماسي وجذاب يناسب: {prompt_text}")
        st.write(f"**طابع الموسيقى:** {music_description}")
        
        speech_text = prepare_text_for_speech(f"موسيقى Saeed MarketAds. {music_description}")
        audio_file = generate_promotional_audio(speech_text, output_path=output_path)
        return audio_file
    except Exception as e:
        st.error(f"حدث خطأ أثناء توليد الموسيقى: {str(e)}")
        return None


# =========================================================
# 8. صانع مقاطع الفيديو القصيرة (Veo / MoviePy Engine)
# =========================================================
def generate_promo_video(audio_path: str, image_path: str = "generated_image.png", output_path: str = "promo_video.mp4"):
    try:
        if not os.path.exists(image_path):
            os.makedirs("assets", exist_ok=True)
            fallback_path = "assets/default_placeholder.png"
            if not os.path.exists(fallback_path):
                url = "https://via.placeholder.com/800x800.png?text=Saeed+MarketAds"
                response = requests.get(url, timeout=10)
                with open(fallback_path, "wb") as f:
                    f.write(response.content)
            image_path = fallback_path

        voice_clip = AudioFileClip(audio_path)
        video_clip = ImageClip(image_path).set_duration(voice_clip.duration)
        video_clip = video_clip.set_audio(voice_clip)
        video_clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

        voice_clip.close()
        video_clip.close()
        return output_path
    except Exception as e:
        st.error(f"حدث خطأ أثناء إنتاج الفيديو: {str(e)}")
        return None

def generate_short_video_agent(prompt_text: str):
    st.info("🎬 جاري معالجة وتوليد الفيديو القصير...")
    
    # 1. محاولة التوليد المباشر عبر نموذج Veo
    try:
        operation = client_main.models.generate_videos(
            model=VEO_MODEL_NAME,
            prompt=prompt_text,
            config=types.GenerateVideosConfig(aspect_ratio="9:16")
        )
        
        with st.spinner("جاري بناء إطارات الفيديو المباشر..."):
            while not operation.done:
                time.sleep(5)
                operation = client_main.operations.get(operation)
        
        if operation.response and operation.response.generated_videos:
            video_uri = operation.response.generated_videos[0].video.uri
            st.video(video_uri)
            st.success("تم توليد الفيديو بنجاح عبر Veo! 🎬")
            return
    except Exception:
        st.caption("ℹ️ الانتقال لنظام الإنتاج المتكامل (صورة تسويقية + صوت مدمج)...")

    # 2. النظام التجميعي الآلي للمقاطع القصيرة (صورة + صوت مدمج في فيديو MP4)
    img_path = generate_image(f"إعلان تسويقي حماسي لـ {prompt_text}")
    script_text = handle_general_chat(f"اكتب سكريبت إعلاني قصير جداً وتنسيقي حماسي بناءً على: {prompt_text}")
    speech_text = prepare_text_for_speech(script_text)
    audio_path = generate_promotional_audio(speech_text, output_path="temp_vid_audio.mp3")

    if audio_path:
        video_file = generate_promo_video(audio_path=audio_path, image_path=img_path or "assets/logo.png")
        if video_file and os.path.exists(video_file):
            with open(video_file, "rb") as vf:
                st.video(vf.read())
            st.success("تم إنتاج وتجميع الفيديو القصير بنجاح! 🎬")


# =========================================================
# 9. موجّه الطلبات (Smart Router)
# =========================================================
def route_user_request(user_input: str) -> str:
    lowered = user_input.lower()
    if any(w in lowered for w in ["صورة", "صور", "توليد صورة", "رسم", "تصميم صورة", "صمم"]):
        return "image_gen"
    elif any(w in lowered for w in ["فيديو", "فيديو قصير", "مقطع فيديو", "صنع فيديو", "انيميشن"]):
        return "video_gen"
    elif any(w in lowered for w in ["موسيقى", "لحن", "موسيقى خلفية", "صوت موسيقي", "أغنية"]):
        return "music_gen"
    elif any(w in lowered for w in ["كوبون", "خصم", "كود", "عروض", "عرض"]):
        return "coupon"
    elif any(w in lowered for w in ["صوت", "سكربت", "تيك توك", "إعلان"]):
        return "voice_script"
    return "general"


# =========================================================
# 10. واجهة المستخدم والتفاعل والأزرار السريعة
# =========================================================
if "quick_action" not in st.session_state:
    st.session_state.quick_action = None

st.markdown("<p style='text-align: right; margin-bottom: 5px; color: #888;'>⚡ اختصارات سريعة:</p>", unsafe_allow_html=True)

# الصف الأول من الاختصارات
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📋 العروض الكبرى", use_container_width=True, key="btn_main_offers"):
        knowledge_data = load_local_coupons()
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

with col2:
    if st.button("🎨 توليد صورة", use_container_width=True, key="btn_main_img"):
        st.session_state.quick_action = "صمم صورة إعلانية مبتكرة لعروض التخفيضات"

with col3:
    if st.button("🎙️ سكريبت صوتي", use_container_width=True, key="btn_main_script"):
        st.session_state.quick_action = "اكتب سكريبت صوتي حماسي لمنتجات شين"

# الصف الثاني من الاختصارات
col4, col5, col6 = st.columns(3)

with col4:
    if st.button("🎬 فيديو قصير", use_container_width=True, key="btn_main_vid"):
        st.session_state.quick_action = "أنشئ فيديو قصير لإعلان خصومات نون"

with col5:
    if st.button("🎵 موسيقى خلفية", use_container_width=True, key="btn_main_music"):
        st.session_state.quick_action = "ولّد موسيقى خلفية حماسية للتسوق"

with col6:
    if st.button("🔥 جملة تسويقية", use_container_width=True, key="btn_main_marketing"):
        st.session_state.quick_action = "اكتب جملة تسويقية مميزة لمتجر علي اكسبريس"


chat_input_val = st.chat_input("اسأل Saeed LogiC عن العروض، أو اطلب صورة، فيديو، موسيقى، سكريبت...")

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
        if selected_agent == "coupon":
            st.markdown("**[وكيل البيانات: Gemma 4]**")
            reply = process_coupon_with_gemma(user_input)
            st.write(reply)
        elif selected_agent == "voice_script":
            st.markdown("**[وكيل الصوت: Gemini]**")
            raw_script = handle_general_chat(f"اكتب سكريبت إعلاني قصير جداً وتنسيقي حماسي بناءً على: {user_input}")
            speech_text = prepare_text_for_speech(raw_script)
            st.write(raw_script)
            generate_promotional_audio(speech_text)
        elif selected_agent == "image_gen":
            st.markdown("**[وكيل الصور: Imagen 3]**")
            generate_image(user_input)
        elif selected_agent == "music_gen":
            st.markdown("**[وكيل الموسيقى: Saeed Audio Agent]**")
            generate_music_track(user_input)
        elif selected_agent == "video_gen":
            st.markdown("**[وكيل الفيديو: Veo / MoviePy Agent]**")
            generate_short_video_agent(user_input)
        else:
            st.markdown("**[مساعد الحوار: Gemini 3.1 Flash Lite]**")
            reply = handle_general_chat(user_input)
            st.write(reply)
            generate_promotional_audio(prepare_text_for_speech(reply))





