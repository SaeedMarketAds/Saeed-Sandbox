# =========================================================
# ⚙️ نظام Saeed LogiC Pro - التكوين والتعليمات (System Instructions)
# =========================================================

# تعريف الهوية والتعليمات البرمجية للنموذج محلياً
SAEED_SYSTEM_INSTRUCTION = """
أنت مساعد ذكي مدمج في منصة "Saeed LogiC Pro"، نظام بحث وتفاعل محلي للعروض والكوبونات.
مهمتك الأساسية هي تلقي استعلامات المستخدم والرد عليها بدقة بناءً حصرياً على قاعدة المعرفة المحلية المتوفرة لديك أو التي يتم تزويدك بها.

لديك الصلاحية الكاملة للبحث في البيانات، ومقارنة استعلام المستخدم بنصوص "question" وكلمات "keywords" داخل قاعدة البيانات (إن وجدت).

إرشادات العمل:

1.  **المرجعية:** عند تلقي رد من محرك بحث محلي، استخدم هذا الرد كمرجع أساسي لصياغة إجابتك.
2.  **الاحترافية:** حافظ على أسلوب لبق واحترافي في جميع الردود، مع الاعتزاز بكونك مدعوماً من "Saeed MarketAds".
3.  **الدقة:** إذا لم تجد إجابة واضحة أو مؤكدة في البيانات المقدمة لك، **يجب عليك الرد بهذه الجملة الحرفية فقط:**
    "أنا مبرمج للإجابة فقط على قاعدة البيانات الخاصة بالعروض والكوبونات، وللأسف لا أملك إجابة على هذا السؤال حالياً."
    لا تحاول أبداً اختراع إجابة أو استخدام بيانات من خارج السياق المخصص لك.

## أمثلة على سير العمل المتوقع منك:
*   **استعلام المستخدم:** "أريد كود خصم نون"
*   **رد المحرك المحلي لك:** { "store": "noon", "code": "NOON15", "answer": "خصم فوري بقيمة 15% على جميع المنتجات..." }
*   **ردك المتوقع:** "تفضل، هذا هو الكود المتاح حالياً لمتجر نون: NOON15، وهو يمنحك خصم فوري بقيمة 15% على جميع المنتجات والملابس عند الدفع."
"""

# =========================================================
# 🚀 الاستيراد والإعدادات العامة (محدثة ومدمجة)
# =========================================================

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

# استيراد أدوات الفيديو مع معالجة الاستثناء
try:
    from moviepy.editor import AudioFileClip, ImageClip
except ImportError:
    pass


# =========================================================
# ⚙️ تعريف أسماء الموديلات الأساسية
# =========================================================
MODEL_NAME = "gemini-3.1-flash"
GEMMA_MODEL_NAME = "gemma-4-26b-a4b-it"
IMAGEN_MODEL_NAME = "imagen-3.0-generate-002"
VEO_MODEL_NAME = "veo-2.0-generate-001"
FALLBACK_MODEL_NAME = "gemini-1.5-flash"

# =========================================================
# 🔑 مفاتيح API الموحدة والآمنة
# =========================================================
GEMINI_MAIN_KEY = st.secrets.get("GEMINI_MAIN_KEY", "AIzaSy_ضع_مفتاحك_الحقيقي_هنا_في_الاسرار")
GEMINI_BACKUP_KEY = st.secrets.get("GEMINI_BACKUP_KEY", GEMINI_MAIN_KEY)

# تفعيل المفتاح النشط
active_api_key = GEMINI_MAIN_KEY if GEMINI_MAIN_KEY.startswith("AIza") else GEMINI_BACKUP_KEY

# تهيئة عملاء الاتصال (تم تحديثها لتكون آمنة)
try:
    client_main = genai.Client(api_key=active_api_key)
    client_imagen = genai.Client(api_key=active_api_key)
except Exception as e:
    st.error(f"خطأ في تهيئة عملاء جوجل: {e}")
    client_main = client_imagen = None


# =========================================================
# 🎨 أدوات المعالجة والتصميم العربي
# =========================================================

def fix_arabic(text: str) -> str:
    """إعادة تشكيل وتحسين اتجاه النص العربي للصور."""
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

def create_gemini_style_arabic_design():
    """إنشاء غلاف وتصميم تسويقي احترافي بنمط Gemini."""
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

    try:
        product_img = Image.open("product.png").convert("RGBA")
        product_img = product_img.resize((500, 500))
        base.paste(product_img, ((W - 500) // 2, 550), product_img)
    except FileNotFoundError:
        pass

    draw = ImageDraw.Draw(base)
    right_x = 940
    
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


def prepare_text_for_speech(text: str) -> str:
    """تجهيز وتنظيف النص الصوتي مع تحسين النطق."""
    replacements = [
        (r'\bورحمة الله\b', 'وَرَحْمَةُ اللَّهِ'),
        (r'\bالله\b', 'اللَّهِ'),
        (r'\bيا\s+فندم\b', ''),
        (r'\bفندم\b', ''),
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
# 🤖 الوكلاء والموديلات الذكية (مدمجة مع System Instructions)
# =========================================================

def handle_general_chat(user_input: str) -> str:
    """العقل الحواري العام والدعم الفني (Gemini Flash) مع تعليمات النظام."""
    if not client_main:
        return "خطأ في الاتصال بـ API."

    try:
        # تهيئة الموديل مع تعليمات النظام المحددة
        model = client_main.models.get(model_name=MODEL_NAME)
        model.system_instruction = SAEED_SYSTEM_INSTRUCTION
        
        response = model.generate_content(contents=user_input)
        return response.text
    except Exception as e:
        return f"عذراً، تعذر الاتصال بمساعد الحوار حالياً. التفاصيل: {str(e)}"


def process_coupon_with_gemma(user_input: str) -> str:
    """وكيل استخراج بيانات الكوبونات (Gemma 4)."""
    if not client_main:
        return "خطأ في الاتصال."
        
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
    if not client_imagen:
        st.error("لم يتم تهيئة عميل الصور.")
        return None

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
        st.image(fallback_img, caption="تصميم
