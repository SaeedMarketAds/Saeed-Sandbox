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

try:
    from moviepy.editor import AudioFileClip, ImageClip
except ImportError:
    pass

# =========================================================
# 🔑 إدارة المفاتيح بشكل آمن وتلافي أخطاء الصلاحية
# =========================================================

MODEL_NAME = "gemini-1.5-flash"  # استخدام موديل مستقر ومتاح للجميع
IMAGEN_MODEL_NAME = "imagen-3.0-generate-002"
VEO_MODEL_NAME = "veo-2.0-generate-001"

# جلب المفاتيح من الـ Secrets مع فحص وجودها
RAW_GEMINI_KEY = st.secrets.get("RAW_GEMINI_KEY", "")
BACKUP_API_KEY = st.secrets.get("BACKUP_API_KEY", "")
PRIMARY_KEY = RAW_GEMINI_KEY or BACKUP_API_KEY

if not PRIMARY_KEY or not PRIMARY_KEY.startswith("AIza"):
    st.error("⚠️ تنبيه هام: يرجى إدخال مفتاح Gemini API صحيح في إعدادات Secrets تحت اسم RAW_GEMINI_KEY لكي يعمل النظام بدون أخطاء.")

# تهيئة العميل البرمجي
client_main = genai.Client(api_key=PRIMARY_KEY if PRIMARY_KEY else "dummy_key")


# =========================================================
# 📂 قاعدة المعرفة والبحث المرن
# =========================================================

def load_local_coupons():
    return {
        "metadata": {
            "platform_name": "Saeed MarketAds",
            "bot_name": "Saeed LogiC Pro"
        },
        "categories": [
            {
                "category_name": "تسوق عام وأزياء",
                "stores": [
                    {
                        "store_name": "نون (Noon)",
                        "keywords": ["نون", "noon", "خصم", "عروض", "كود"],
                        "coupons": [
                            {"code": "NOON15", "description": "خصم فوري بقيمة 15٪ على جميع المنتجات والملابس."}
                        ]
                    },
                    {
                        "store_name": "شي إن (SHEIN)",
                        "keywords": ["شي إن", "shein", "ملابس", "فساتين", "شي ان", "عروض", "كود"],
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
                        "keywords": ["علي إكسبريس", "aliexpress", "علي اكسبريس", "إلكترونيات", "عروض", "كود"],
                        "coupons": [
                            {"code": "ALI50", "description": "خصم يصل إلى 50٪ على الأجهزة الإلكترونية وإكسسوارات الهواتف."}
                        ]
                    }
                ]
            }
        ]
    }


def process_coupon_from_knowledge(user_input: str) -> str:
    knowledge_data = load_local_coupons()
    lowered_input = user_input.lower().strip()
    
    found_coupons = []
    categories = knowledge_data.get("categories", [])
    
    # إذا طلب المستخدم "عروض" بشكل عام، اعرض كل الكوبونات المتاحة مباشرة
    if any(w in lowered_input for w in ["عرض", "عروض", "كوبون", "كوبونات", "تخفيض"]):
        for cat in categories:
            for store in cat.get("stores", []):
                store_name = store.get("store_name", "")
                for coupon in store.get("coupons", []):
                    found_coupons.append(f"🏷️ **المتجر:** {store_name}\n🔑 **الكود:** `{coupon.get('code')}`\n📝 **الوصف:** {coupon.get('description')}\n")
    else:
        # البحث المخصص حسب الكلمات
        for cat in categories:
            for store in cat.get("stores", []):
                store_name = store.get("store_name", "")
                store_keywords = [k.lower() for k in store.get("keywords", [])]
                if any(kw in lowered_input for kw in store_keywords) or any(s.lower() in lowered_input for s in store_name.lower().split()):
                    for coupon in store.get("coupons", []):
                        found_coupons.append(f"🏷️ **المتجر:** {store_name}\n🔑 **الكود:** `{coupon.get('code')}`\n📝 **الوصف:** {coupon.get('description')}\n")

    if found_coupons:
        return "إليك الكوبونات والعروض المتاحة:\n\n" + "\n".join(found_coupons)
    
    return "عذراً، لم أجد كوبوناً مطابهاً تماماً لطلبك. يمكنك طلب (العروض الكبرى) لرؤية كافة التخفيضات المتاحة!"


def handle_general_chat(user_input: str) -> str:
    prompt = f"أنت مساعد التسوق الذكي لشبكة Saeed MarketAds. أجب باختصار ولباقة على: {user_input}"
    try:
        response = client_main.models.generate_content(model=MODEL_NAME, contents=prompt)
        return response.text
    except Exception as e:
        return f"عذراً، يجدر التحقق من صلاحية مفتاح الـ API الخاص بـ Gemini. التفاصيل: {str(e)}"


# =========================================================
# 🖥️ واجهة المستخدم (Streamlit UI)
# =========================================================

st.set_page_config(page_title="Saeed LogiC Pro", page_icon="🚀", layout="centered")
st.title("Saeed LogiC Pro 🚀")
st.subheader("النظام التفاعلي لإدارة العروض والتسويق الذكي")

if "quick_action" not in st.session_state:
    st.session_state.quick_action = None

st.markdown("<p style='text-align: right; margin-bottom: 5px; color: #888;'>⚡ اختصارات سريعة:</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("📋 العروض الكبرى", use_container_width=True, key="btn_main_offers"):
        knowledge_data = load_local_coupons()
        st.success("🎉 أحدث العروض والكوبونات المتاحة:")
        for cat in knowledge_data.get("categories", []):
            st.markdown(f"### 📂 {cat.get('category_name')}")
            for store in cat.get("stores", []):
                st.markdown(f"**{store.get('store_name')}**")
                for coupon in store.get("coupons", []):
                    st.code(coupon.get('code'), language="text")
                    st.write(coupon.get('description'))
                st.divider()

with col2:
    if st.button("🔥 عرض عروض نون وشي إن", use_container_width=True, key="btn_main_noon"):
        st.session_state.quick_action = "عروض"


chat_input_val = st.chat_input("اسأل Saeed LogiC عن العروض (مثال: عروض، نون، شي إن)...")

user_input = None
if chat_input_val:
    user_input = chat_input_val
elif st.session_state.quick_action:
    user_input = st.session_state.quick_action
    st.session_state.quick_action = None

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
        
    with st.chat_message("assistant"):
        st.markdown("**[وكيل البيانات: Saeed LogiC Knowledge]**")
        reply = process_coupon_from_knowledge(user_input)
        st.write(reply)
