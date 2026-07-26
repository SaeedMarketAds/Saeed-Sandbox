# Import warnings
import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)

import json
import os
import re
import io
import time
import asyncio
import streamlit as st
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from google import genai
from google.genai import types
import edge_tts
import arabic_reshaper
from bidi.algorithm import get_display

# استيراد أدوات الفيديو مع معالجة الاستثناء في حال عدم توفرها
try:
    from moviepy.editor import AudioFileClip, ImageClip
except ImportError:
    pass

# =========================================================
# 🔑 الإعدادات وتوحيد مفاتيح وبنية الموديلات المحدثة
# =========================================================

MODEL_NAME = "gemini-2.5-flash"
FALLBACK_MODEL_NAME = "gemini-1.5-flash"
IMAGEN_MODEL_NAME = "imagen-3.0-generate-002"
VEO_MODEL_NAME = "veo-2.0-generate-001"

# قراءة المفاتيح الصحيحة حصرياً من Streamlit Secrets مع تأمين البدائل الحقيقية
BACKUP_API_KEY = st.secrets.get("BACKUP_API_KEY", "")
IMAGEN_API_KEY = st.secrets.get("IMAGEN_API_KEY", "")
RAW_GEMINI_KEY = st.secrets.get("RAW_GEMINI_KEY", "")
RAW_AUDIO_KEY = st.secrets.get("RAW_AUDIO_KEY", "")

# توحيد المفتاح النشط الفعلي لعمل العميل البرمجي لضمان عدم ظهور أخطاء الصلاحية
PRIMARY_KEY = RAW_GEMINI_KEY or BACKUP_API_KEY
AUDIO_KEY = RAW_AUDIO_KEY or PRIMARY_KEY
IMAGEN_KEY = IMAGEN_API_KEY if IMAGEN_API_KEY.startswith("AIza") else PRIMARY_KEY

# تهيئة العملاء الموحدين بمفاتيح حقيقية وسليمة
client_main = genai.Client(api_key=PRIMARY_KEY)
client_audio = genai.Client(api_key=AUDIO_KEY)
client_imagen = genai.Client(api_key=IMAGEN_KEY)


# =========================================================
# 🎨 أدوات المعالجة والتصميم العربي
# =========================================================

def fix_arabic(text: str) -> str:
    """إعادة تشكيل وتحسين اتجاه النص العربي للصور."""
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

def create_gemini_style_arabic_design():
    """إنشاء غلاف وتصميم تسويقي احترافي بنمط Saeed MarketAds."""
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
    card_draw.rounded_rectangle([80, 200, 1000, 1720], radius=40, fill=(255, 255, 255, 20), outline=(255, 255, 255, 55), width=3)
    base = Image.alpha_composite(base, card_layer)

    try:
        title_font = ImageFont.truetype("Cairo-Bold.ttf", 60)
        sub_font = ImageFont.truetype("Cairo-Regular.ttf", 32)
        badge_font = ImageFont.truetype("Cairo-Bold.ttf", 24)
        button_font = ImageFont.truetype("Cairo-Bold.ttf", 36)
    except OSError:
        title_font = sub_font = badge_font = button_font = ImageFont.load_default()

    draw = ImageDraw.Draw(base)
    right_x = 940
    
    badge_text = fix_arabic("إصدار محدود 2026")
    draw.rounded_rectangle([right_x - 220, 260, right_x, 310], radius=12, fill=(99, 102, 241, 230))
    draw.text((right_x - 200, 272), badge_text, font=badge_font, fill="white")
    
    draw.text((right_x - 550, 360), fix_arabic("عروض Saeed MarketAds"), font=title_font, fill="white")
    draw.text((right_x - 620, 460), fix_arabic("تجربة تسوق رقمية ذكية ومتكاملة"), font=sub_font, fill=(226, 232, 240))
    
    btn_w = 300
    btn_rect = [(W - btn_w) // 2, 1150, (W + btn_w) // 2, 1230]
    draw.rounded_rectangle(btn_rect, radius=20, fill=(236, 72, 153, 255))
    draw.text((btn_rect[0] + 65, 1168), fix_arabic("اطلب الآن"), font=button_font, fill="white")
    
    return base.convert("RGB")


def prepare_text_for_speech(text: str) -> str:
    """تجهيز وتنظيف النص الصوتي مع تحسين النطق للكلمات العربية والإنجليزية."""
    replacements = [
        (r'\bورحمة الله\b', 'وَرَحْمَةُ اللَّهِ'),
        (r'\bالله\b', 'اللَّهِ'),
        (r'\bSaeed\s+LogiC\s+Pro\b', 'سَعِيد لُوجِيك بْرُو'),
        (r'\bSaeed\s+MarketAds\b', 'سَعِيد مَارْكِت أَدْس'),
        (r'\bSHEIN\b', 'شِي إن'),
        (r'\bAliExpress\b', 'عَلِي إكْسِبْرِيس'),
        (r'\bNoon\b', 'نُون'),
    ]
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    text = re.sub(r'[*#_~`>\[\]\(\)]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def clean_text_for_speech(text: str) -> str:
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\(.*?\)', '', text)
    text = re.sub(r'#+', '', text)
    return text.strip()


# =========================================================
# 📂 إدارة البيانات المحلية وقاعدة المعرفة
# =========================================================

def load_local_coupons():
    """قراءة قاعدة المعرفة وتوفير هيكل افتراضي شامل في حال عدم وجود الملف."""
    file_paths = ["knowledge.json", "data/knowledge.json"]
    for path in file_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
                
    # هيكل افتراضي شامل ومحدث يعمل مباشرة من قاعدة المعرفة البرمجية
    return {
        "metadata": {
            "platform_name": "Saeed MarketAds",
            "bot_name": "Saeed LogiC Pro Enterprise",
            "version": "3.0.0"
        },
        "categories": [
            {
                "category_name": "تسوق عام وأزياء",
                "stores": [
                    {
                        "store_name": "نون (Noon)",
                        "keywords": ["نون", "noon", "خصم نون", "كود نون"],
                        "coupons": [
                            {"code": "NOON15", "description": "خصم فوري بقيمة 15٪ على جميع المنتجات والملابس."}
                        ]
                    },
                    {
                        "store_name": "شي إن (SHEIN)",
                        "keywords": ["شي إن", "shein", "ملابس", "فساتين", "شي ان"],
                        "coupons": [
                            {"code": "SHEIN30", "description": "خصم 30٪ على الفساتين والملابس الصيفية الجديدة."},
                            {"code": "N73QS", "description": "خصم 30% للمستخدمين الجدد، يربط المتسوق بمختاراتك الخاصة."}
                        ]
                    }
                ]
            },
            {
                "category_name": "الإلكترونيات",
                "stores": [
                    {
                        "store_name": "علي إكسبريس (AliExpress)",
                        "keywords": ["علي إكسبريس", "aliexpress", "علي اكسبريس", "إلكترونيات"],
                        "coupons": [
                            {"code": "ALI50", "description": "خصم يصل إلى 50٪ على الأجهزة الإلكترونية وإكسسوارات الهواتف."}
                        ]
                    }
                ]
            }
        ]
    }


# =========================================================
# 🤖 الوكلاء والموديلات الذكية
# =========================================================

def handle_general_chat(user_input: str) -> str:
    """العقل الحواري العام والدعم الفني (Gemini Flash مع نظام الطوارئ)."""
    prompt = (
        f"أنت (Saeed LogiC Pro)، مساعد التسوق الذكي واللبق والمطور خصيصاً "
        f"لصالح منصة وشبكة (Saeed MarketAds) الرائدة في العروض والتسويق الرقمي.\n"
        f"أجب على العميل باختصار، وبلباقة ترحيبية عالية، واحترافية تامة.\n"
        f"الطلب: {user_input}"
    )
    try:
        response = client_main.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return response.text
    except Exception:
        try:
            response = client_main.models.generate_content(
                model=FALLBACK_MODEL_NAME,
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"عذراً، تعذر الاتصال بمساعد الحوار حالياً. التفاصيل: {str(e)}"


def process_coupon_from_knowledge(user_input: str) -> str:
    """وكيل استخراج بيانات الكوبونات والعروض من قاعدة المعرفة بذكاء."""
    knowledge_data = load_local_coupons()
    lowered_input = user_input.lower()
    
    found_coupons = []
    categories = knowledge_data.get("categories", [])
    for cat in categories:
        for store in cat.get("stores", []):
            store_name = store.get("store_name", "")
            store_keywords = [k.lower() for k in store.get("keywords", [])]
            
            # فحص المطابقة مع المتجر أو الكلمات المفتاحية
            if any(kw in lowered_input for kw in store_keywords) or any(s.lower() in lowered_input for s in store_name.lower().split()):
                for coupon in store.get("coupons", []):
                    found_coupons.append(f"🏷️ **المتجر:** {store_name}\n🔑 **الكود:** `{coupon.get('code')}`\n📝 **الوصف:** {coupon.get('description')}\n")

    if found_coupons:
        return "إليك الكوبونات والعروض المطابقة لطلبك من قاعدة المعرفة:\n\n" + "\n".join(found_coupons)
    
    # إذا لم يتم العثور على مطابقة مباشرة، يتم الاستعانة بالذكاء الاصطناعي لتحليل قاعدة المعرفة
    prompt = (
        f"بناءً على قاعدة المعرفة الخاصة بـ Saeed MarketAds:\n{json.dumps(knowledge_data, ensure_ascii=False)}\n"
        f"أجب بدقة على طلب العميل التالي واستخرج الكود أو العرض المناسب: {user_input}.\n"
        f"إذا لم تجد، أجب باختصار: (لم أجد كوبوناً متاحاً لهذا الطلب حالياً)."
    )
    try:
        response = client_main.models.generate_content(model=MODEL_NAME, contents=prompt)
        return response.text.strip()
    except Exception:
        return "لم أجد كوبوناً متاحاً لهذا الطلب حالياً."


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
    """مولد الصور المعتمد باستخدام Imagen 3 مع خيار محلي احتياطي متقدم."""
    try:
        st.info("🎨 جاري تصميم الصورة عبر Imagen 3...")
        response = client_imagen.models.generate_images(
            model=IMAGEN_MODEL_NAME,
            prompt=f"Professional commercial product advertisement, {prompt}",
            config=dict(number_of_images=1, output_mime_type="image/jpeg", aspect_ratio="1:1")
        )
        for generated_image in response.generated_images:
            image_path = "generated_output.png"
            image = Image.open(io.BytesIO(generated_image.image.image_bytes))
            image.save(image_path)
            st.image(image, caption="الصورة الناتجة 🎨", use_container_width=True)
            return image_path
    except Exception:
        st.warning("⚠️ جاري التوليد الاحترافي للتصميم المحلي لشبكة Saeed MarketAds...")
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
        return generate_promotional_audio(speech_text, output_path=output_path)
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
    try:
        operation = client_main.models.generate_videos(
            model=VEO_MODEL_NAME, prompt=prompt_text, config=types.GenerateVideosConfig(aspect_ratio="9:16")
        )
        with st.spinner("جاري بناء إطارات الفيديو..."):
            while not operation.done:
                time.sleep(5)
                operation = client_main.operations.get(operation)
        if operation.response and operation.response.generated_videos:
            video_uri = operation.response.generated_videos[0].video.uri
            st.video(video_uri)
            st.success("تم توليد الفيديو بنجاح عبر Veo! 🎬")
            return
    except Exception:
        pass

    # النظام التجميعي الاحتياطي (صورة + صوت مدمج)
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
    if any(w in lowered for w in ["صورة", "صور", "رسم", "تصميم"]):
        return "image_gen"
    elif any(w in lowered for w in ["فيديو", "مقطع", "انيميشن"]):
        return "video_gen"
    elif any(w in lowered for w in ["موسيقى", "لحن", "أغنية"]):
        return "music_gen"
    elif any(w in lowered for w in ["كوبون", "خصم", "كود", "عروض", "عرض", "نون", "شي إن", "علي اكسبريس"]):
        return "coupon"
    elif any(w in lowered for w in ["صوت", "سكربت", "إعلان"]):
        return "voice_script"
    return "general"


# =========================================================
# 🖥️ واجهة المستخدم (Streamlit UI)
# =========================================================

st.set_page_config(page_title="Saeed LogiC Pro", page_icon="🚀", layout="centered")
st.title("Saeed LogiC Pro 🚀")
st.subheader("النظام التفاعلي لإدارة العروض والصوت والصور والفيديو والموسيقى")

if "quick_action" not in st.session_state:
    st.session_state.quick_action = None

st.markdown("<p style='text-align: right; margin-bottom: 5px; color: #888;'>⚡ اختصارات سريعة:</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📋 العروض الكبرى", use_container_width=True, key="btn_main_offers"):
        knowledge_data = load_local_coupons()
        st.success("🎉 أحدث العروض والكوبونات من قاعدة المعرفة:")
        for cat in knowledge_data.get("categories", []):
            st.markdown(f"### 📂 {cat.get('category_name')}")
            for store in cat.get("stores", []):
                st.markdown(f"**{store.get('store_name')}**")
                for coupon in store.get("coupons", []):
                    st.code(coupon.get('code'), language="text")
                    st.write(coupon.get('description'))
                st.divider()

with col2:
    if st.button("🎨 توليد صورة", use_container_width=True, key="btn_main_img"):
        st.session_state.quick_action = "صمم صورة إعلانية مبتكرة لعروض التخفيضات"

with col3:
    if st.button("🎙️ سكريبت صوتي", use_container_width=True, key="btn_main_script"):
        st.session_state.quick_action = "اكتب سكريبت صوتي حماسي لمنتجات شين"

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
            st.markdown("**[وكيل البيانات: Knowledge Base & Gemini]**")
            with st.spinner("جاري جلب أحدث الكوبونات من قاعدة المعرفة... 🔍"):
                reply = process_coupon_from_knowledge(user_input)
                st.write(reply)

        elif selected_agent == "voice_script":
            st.markdown("**[وكيل الصوت: Gemini & Edge-TTS]**")
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
            st.markdown("**[مساعد الحوار: Gemini 2.5 Flash]**")
            reply = handle_general_chat(user_input)
            st.write(reply)
            generate_promotional_audio(prepare_text_for_speech(reply))

