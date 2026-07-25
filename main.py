import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)

# =========================================================
# 1. مكتبات بايثون الأساسية (Standard Library)
# =========================================================
import asyncio
import io
import json
import os
import re
import time

# =========================================================
# 2. المكتبات الخارجية (Third-Party Libraries)
# =========================================================
import arabic_reshaper
from bidi.algorithm import get_display
import edge_tts
from google import genai
from google.genai import types
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# Streamlit واختصارات مكوناته
import streamlit as st
import streamlit.components.v1 as components

# =========================================================
# 3. استيراد اختياري مع معالجة الاستثناءات
# =========================================================
# استيراد أدوات الفيديو مع معالجة الاستثناء في حال عدم توفرها
try:
    from moviepy.editor import AudioFileClip, ImageClip
except ImportError:
    pass



# =========================================================
# 🔑 الإعدادات وتوحيد مفاتيح وبنية الموديلات
# =========================================================

MODEL_NAME = "gemini-3.1-flash-lite"
GEMMA_MODEL_NAME = "gemma-4-26b-a4b-it"
IMAGEN_MODEL_NAME = "imagen-3.0-generate-002"
VEO_MODEL_NAME = "veo-2.0-generate-001"

# قراءة المفاتيح من Streamlit Secrets مع خيارات الطوارئ
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
AUDIO_API_KEY = st.secrets.get("AUDIO_API_KEY", "")
BACKUP_API_KEY = st.secrets.get("BACKUP_API_KEY", "")
IMAGEN_API_KEY = st.secrets.get("IMAGEN_API_KEY", "")

# توحيد المفتاح النشط لجميع الموديلات
PRIMARY_KEY = GEMINI_API_KEY or BACKUP_API_KEY
AUDIO_KEY = AUDIO_API_KEY or PRIMARY_KEY
IMAGEN_KEY = IMAGEN_API_KEY or PRIMARY_KEY

# تهيئة العملاء الموحدين
client_main = genai.Client(api_key=PRIMARY_KEY)
client_audio = genai.Client(api_key=AUDIO_KEY)
client_imagen = genai.Client(api_key=IMAGEN_KEY)

import urllib.request

# =========================================================
# 🎨 أدوات المعالجة والتصميم العربي والدعم الديناميكي
# =========================================================
# =========================================================
# 🛠️ دوال معالجة النصوص والصوت
# =========================================================

def clean_text_for_speech(text: str) -> str:
    """تنظيف النص من رموز Markdown والروابط قبل تحويله لـ TTS."""
    if not text:
        return ""
    clean_text = re.sub(r'http\S+', '', text)
    clean_text = re.sub(r'[*_~`#\-]', '', clean_text)
    return clean_text.strip()

# ربط الاسم الآخر بالدالة لضمان توافق جميع استدعاءات الكود
prepare_text_for_speech = clean_text_for_speech


def fix_arabic(text: str) -> str:
    """معالجة وتعديل النص العربي للعرض الصحيح على الصور."""
    if not text:
        return ""
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except Exception:
        return text


=========================================================

def get_arabic_font(size: int):
    """جلب وتحميل الخط العربي تلقائياً لضمان عدم ظهور المربعات في السيرفر."""
    font_path = "Cairo-Bold.ttf"
    if not os.path.exists(font_path):
        try:
            url = "https://raw.githubusercontent.com/google/fonts/main/ofl/cairo/static/Cairo-Bold.ttf"
            urllib.request.urlretrieve(url, font_path)
        except Exception:
            pass
    try:
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()


def create_gemini_style_arabic_design(
    title="خصومات نون الحصرية",
    subtitle="أقوى العروض والتخفيضات اليوم",
    badge="خصم خاص"
):
    """إنشاء غلاف وتصميم تسويقي ديناميكي مع كتابة نصوص عربية واضحة."""
    W, H = 1080, 1920
    base = Image.new("RGBA", (W, H), (15, 23, 42, 255))

    # طبقة الإضاءة (Glow Effects)
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    glow_draw.ellipse([50, 100, 750, 800], fill=(99, 102, 241, 150))
    glow_draw.ellipse([600, 1200, 1150, 1750], fill=(236, 72, 153, 130))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(100))
    base = Image.alpha_composite(base, glow_layer)

    # البطاقة الزجاجية
    card_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    card_draw = ImageDraw.Draw(card_layer)
    card_draw.rounded_rectangle([80, 200, 1000, 1720], radius=40, fill=(255, 255, 255, 20), outline=(255, 255, 255, 55), width=2)
    base = Image.alpha_composite(base, card_layer)

    # جلب الخطوط
    title_font = get_arabic_font(60)
    sub_font = get_arabic_font(40)
    badge_font = get_arabic_font(32)

    draw = ImageDraw.Draw(base)

    # رسم الشارة (Badge)
    if badge:
        badge_text = fix_arabic(badge)
        draw.rectangle([700, 260, 950, 330], fill=(236, 72, 153, 255))
        draw.text((825, 295), badge_text, font=badge_font, fill=(255, 255, 255, 255), anchor="mm")

    # رسم العنوان الرئيسي
    if title:
        title_text = fix_arabic(title)
        draw.text((540, 500), title_text, font=title_font, fill=(255, 255, 255, 255), anchor="mm")

    # رسم العنوان الفرعي
    if subtitle:
        sub_text = fix_arabic(subtitle)
        draw.text((540, 620), sub_text, font=sub_font, fill=(226, 232, 240, 255), anchor="mm")

    return base
    

def create_gemini_style_arabic_design(
    title="خصومات نون الحصرية", 
    subtitle="أقوى العروض والتخفيضات اليوم", 
    badge="خصم خاص"
):
    """إنشاء غلاف وتصميم تسويقي ديناميكي يتكيف مع الطلب بنمط احترافي."""
    W, H = 1080, 1920
    base = Image.new("RGBA", (W, H), (15, 23, 42, 255))
    
    # طبقة الإضاءة (Glow Effects)
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    glow_draw.ellipse([50, 100, 750, 800], fill=(99, 102, 241, 150))
    glow_draw.ellipse([600, 1200, 1150, 1750], fill=(236, 72, 153, 130))
    glow_draw.ellipse([W // 2 - 250, H // 2 - 250, W // 2 + 250, H // 2 + 250], fill=(14, 165, 233, 90))
    
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(100))
    base = Image.alpha_composite(base, glow_layer)
    
    # البطاقة الزجاجية
    card_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    card_draw = ImageDraw.Draw(card_layer)
    card_draw.rounded_rectangle([80, 200, 1000, 1720], radius=40, fill=(255, 255, 255, 20), outline=(255, 255, 255, 55), width=3)
    base = Image.alpha_composite(base, card_layer)

    # جلب الخطوط العربية الصحيحة
    title_font = get_arabic_font(52)
    sub_font = get_arabic_font(30)
    badge_font = get_arabic_font(24)
    button_font = get_arabic_font(34)

    try:
        product_img = Image.open("product.png").convert("RGBA")
        product_img = product_img.resize((500, 500))
        base.paste(product_img, ((W - 500) // 2, 550), product_img)
    except FileNotFoundError:
        pass

    draw = ImageDraw.Draw(base)
    right_x = 940
    
    # رسم الشارة والعناوين بالنصوص الديناميكية
    badge_text = fix_arabic(badge)
    draw.rounded_rectangle([right_x - 240, 260, right_x, 310], radius=12, fill=(99, 102, 241, 230))
    draw.text((right_x - 220, 272), badge_text, font=badge_font, fill="white")
    
    draw.text((right_x - 750, 360), fix_arabic(title), font=title_font, fill="white")
    draw.text((right_x - 750, 450), fix_arabic(subtitle), font=sub_font, fill=(226, 232, 240))
    
    btn_w = 320
    btn_rect = [(W - btn_w) // 2, 1150, (W + btn_w) // 2, 1230]
    draw.rounded_rectangle(btn_rect, radius=20, fill=(236, 72, 153, 255))
    draw.text((btn_rect[0] + 60, 1168), fix_arabic("تسوق الآن"), font=button_font, fill="white")
    
    return base.convert("RGB")


def generate_image(prompt: str) -> str:
    """توليد الصورة وتفعيل الاحتياطي الديناميكي بالنصوص المطلوبة."""
    try:
        st.info("🎨 ...جاري تصميم الصورة")
        response = client_imagen.models.generate_images(
            model=IMAGEN_MODEL_NAME,
            prompt=f"Professional commercial product advertisement, {prompt}",
            config=dict(
                number_of_images=1,
                output_mime_type="image/jpeg",
                aspect_ratio="1:1"
            )
        )
        for generated_image in response.generated_images:
            image_path = "generated_output.png"
            image = Image.open(io.BytesIO(generated_image.image.image_bytes))
            image.save(image_path)
            st.image(image, caption="الصورة الناتجة 🎨", use_container_width=True)
            return image_path

    except Exception:
        st.warning("⚠️ ...جاري التوليد المحلي الاحترافي للتصميم")
        
        # استخراج العنوان من طلب المستخدم أو افتراضي
        title_text = prompt[:30] if prompt else "عرض خاص"
        
        fallback_img = create_gemini_style_arabic_design(
            title=title_text, 
            subtitle="أحدث العروض والكوبونات المتاحة",
            badge="عروض حصرية"
        )
        fallback_path = "generated_output.png"
        fallback_img.save(fallback_path)
        st.image(fallback_img, caption="تصميم احترافي", use_container_width=True)
        return fallback_path
# =========================================================
# 🎨 واجهة صانع الإعلانات
# =========================================================

def render_ad_builder_ui():
    """عرض واجهة صانع الإعلانات التفاعلية."""
    st.markdown("### 🎨 صانع الإعلانات التفاعلية")
    
    prompt_input = st.text_input("أدخل وصف الإعلان أو المنتج:", placeholder="مثال: خصومات حصرية على المنتجات")
    
    if st.button("توليد التصميم 🚀"):
        if prompt_input:
            generate_image(prompt_input)
        else:
            st.warning("يرجى إدخال نص أولاً!")






# =========================================================
# 📂 إدارة البيانات المحلية
# =========================================================

def load_local_coupons():
    file_paths = ["knowledge.json", "data/knowledge.json"]
    for path in file_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                return {"error": f"حدث خطأ أثناء قراءة قاعدة المعرفة: {str(e)}"}
    return {"error": "لم يتم العثور على ملف قاعدة المعرفة knowledge.json"}


# =========================================================
# 🤖 الوكلاء والموديلات الذكية
# =========================================================

def handle_general_chat(user_input: str) -> str:
    """العقل الحواري العام والدعم الفني (Gemini Flash Lite)."""
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


def process_coupon_with_gemma(user_input: str) -> str:
    """وكيل استخراج بيانات الكوبونات (Gemma 4)."""
    coupons_data = load_local_coupons()
    prompt = (
        f"أنت وكيل البيانات المسؤول عن قواعد عروض Saeed MarketAds.\n"
        f"بناءً على قاعدة البيانات المحلية التالية:\n{json.dumps(coupons_data, ensure_ascii=False)}\n"
        f"استخرج كود الخصم الدقيق وتفاصيله للرد على طلب العميل: {user_input}.\n"
        f"إذا لم تجد كوداً مناسباً، قل باختصار ولباقة: (لم أجد كوبوناً متاحاً لهذا الطلب حالياً)."
    )
    try:
        response = client_main.models.generate_content(
            model=GEMMA_MODEL_NAME,
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"عذراً، تعذر جلب معلومات الكوبون. التفاصيل: {str(e)}"


async def _text_to_speech_async(text: str, output_path: str):
    voice = "ar-SA-HamedNeural"
    clean_text = clean_text_for_speech(text)
    communicate = edge_tts.Communicate(clean_text, voice)
    await communicate.save(output_path)


def generate_promotional_audio(text_script: str, output_path: str = "promo_voice.mp3") -> str:
    """مولد التعليق الصوتي الإعلاني."""
    try:
        asyncio.run(_text_to_speech_async(text_script, output_path))
        with open(output_path, "rb") as f:
            st.audio(f.read(), format="audio/mp3")
        st.success("تم توليد التعليق الصوتي بنجاح! 🎙")
        return output_path
    except Exception as e:
        st.error(f"حدث خطأ أثناء توليد الصوت: {str(e)}")
        return None


def generate_image(prompt: str) -> str:
    """مولد الصور المعتمد باستخدام Imagen 3 مع خيار محلي احتياطي."""
    try:
        st.info("🎨 جاري تصميم الصورة...")
        response = client_imagen.models.generate_images(
            model=IMAGEN_MODEL_NAME,
            prompt=f"Professional commercial product advertisement, {prompt}",
            config=dict(
                number_of_images=1,
                output_mime_type="image/jpeg",
                aspect_ratio="1:1"
            )
        )
        for generated_image in response.generated_images:
            image_path = "generated_output.png"
            image = Image.open(io.BytesIO(generated_image.image.image_bytes))
            image.save(image_path)
            st.image(image, caption="الصورة الناتجة 🎨", use_container_width=True)
            return image_path
            
    except Exception:
        st.warning("⚠️ جاري التوليد المحلي الاحترافي للتصميم...")
        fallback_img = create_gemini_style_arabic_design()
        fallback_path = "generated_output.png"
        fallback_img.save(fallback_path)
        st.image(fallback_img, caption="تصميم Saeed MarketAds الاحترافي", use_container_width=True)
        return fallback_path


def generate_music_track(prompt_text: str, output_path: str = "promo_music.mp3") -> str:
    """مولد الموسيقى والنغمات التسويقية."""
    try:
        st.info("🎵 جاري إنشاء النغمة والموسيقى التسويقية...")
        music_description = handle_general_chat(f"وصف موسيقي تسويقي حماسي وجذاب يناسب: {prompt_text}")
        st.write(f"**طابع الموسيقى:** {music_description}")
        
        speech_text = prepare_text_for_speech(f"موسيقى Saeed MarketAds. {music_description}")
        audio_file = generate_promotional_audio(speech_text, output_path=output_path)
        return audio_file
    except Exception as e:
        st.error(f"حدث خطأ أثناء توليد الموسيقى: {str(e)}")
        return None


def generate_promo_video(audio_path: str, image_path: str = "generated_output.png", output_path: str = "promo_video.mp4"):
    """دمج الصورة والصوت لإنشاء فيديو MP4."""
    try:
        if not os.path.exists(image_path):
            img = Image.new("RGB", (800, 800), color=(30, 41, 59))
            img.save(image_path)

        voice_clip = AudioFileClip(audio_path)
        video_clip = ImageClip(image_path).set_duration(voice_clip.duration)
        video_clip = video_clip.set_audio(voice_clip)
        video_clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

        voice_clip.close()
        video_clip.close()
        return output_path
    except Exception as e:
        st.error(f"حدث خطأ أثناء تجميع الفيديو: {str(e)}")
        return None


def generate_short_video_agent(prompt_text: str):
    """وكيل توليد الفيديوهات القصيرة (Veo / MoviePy Engine)."""
    st.info("🎬 جاري معالجة وتوليد الفيديو القصير...")
    
    # 1. التوليد عبر Veo
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

    # 2. النظام التجميعي الاحتياطي
    img_path = generate_image(f"إعلان تسويقي حماسي لـ {prompt_text}")
    script_text = handle_general_chat(f"اكتب سكريبت إعلاني قصير جداً وتنسيقي حماسي بناءً على: {prompt_text}")
    speech_text = prepare_text_for_speech(script_text)
    audio_path = generate_promotional_audio(speech_text, output_path="temp_vid_audio.mp3")

    if audio_path:
        video_file = generate_promo_video(audio_path=audio_path, image_path=img_path or "generated_output.png")
        if video_file and os.path.exists(video_file):
            with open(video_file, "rb") as vf:
                st.video(vf.read())
            st.success("تم إنتاج وتجميع الفيديو القصير بنجاح! 🎬")


# =========================================================
# 🔀 موجه الطلبات الذكي (Smart Router)
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
# 🖥️ واجهة المستخدم (Streamlit UI)
# =========================================================

st.set_page_config(page_title="Saeed LogiC Pro", page_icon="🚀", layout="centered")
st.title("Saeed LogiC Pro 🚀")
st.subheader("النظام التفاعلي الموحد لإدارة العروض والصوت والصور والفيديو والموسيقى")

# 📍 استدعاء واجهة صانع الإعلانات التفاعلية هنا
render_ad_builder_ui()

if "quick_action" not in st.session_state:
    st.session_state.quick_action = None

st.markdown("<p style='text-align: right; margin-bottom: 5px; color: #888;'>⚡ اختصارات سريعة:</p>", unsafe_allow_html=True)

# الصف الأول
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

# الصف الثاني
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


# استقبال المدخلات والتوظيف الموحد
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
            with st.spinner("جاري البحث عن أحدث البيانات والكوبونات... 🔍"):
                reply = process_coupon_with_gemma(user_input)
                st.write(reply)

        elif selected_agent == "voice_script":
            st.markdown("**[وكيل الصوت: Gemini]**")
            with st.spinner("جاري كتابة السكريبت وتوليد الصوت... 🎙️"):
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
