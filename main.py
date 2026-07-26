import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)

import json
import os
import re
import streamlit as st
from google import genai

# =========================================================
# 🔑 إعدادات الموديل والمفاتيح
# =========================================================

MODEL_NAME = "gemini-1.5-flash"

RAW_GEMINI_KEY = st.secrets.get("RAW_GEMINI_KEY", "")
BACKUP_API_KEY = st.secrets.get("BACKUP_API_KEY", "")
PRIMARY_KEY = RAW_GEMINI_KEY or BACKUP_API_KEY

# تهيئة العميل البرمجي (حتى لو لم يتوفر مفتاح، يتم وضع مفتاح مؤقت لتجنب انهيار التطبيق عند البدء)
client_main = genai.Client(api_key=PRIMARY_KEY if PRIMARY_KEY and PRIMARY_KEY.startswith("AIza") else "dummy_key")


# =========================================================
# 📂 قاعدة المعرفة المحلية (البديلة)
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


def search_knowledge_base(user_input: str) -> str:
    """البحث في قاعدة المعرفة المحلية في حال عدم توفر أو فشل الـ API"""
    knowledge_data = load_local_coupons()
    lowered_input = user_input.lower().strip()
    
    found_coupons = []
    categories = knowledge_data.get("categories", [])
    
    if any(w in lowered_input for w in ["عرض", "عروض", "كوبون", "كوبونات", "خصم", "تخفيض", "كل", "الكبرى"]):
        for cat in categories:
            for store in cat.get("stores", []):
                store_name = store.get("store_name", "")
                for coupon in store.get("coupons", []):
                    found_coupons.append(f"🏷️ **المتجر:** {store_name}\n🔑 **الكود:** `{coupon.get('code')}`\n📝 **الوصف:** {coupon.get('description')}\n")
    else:
        for cat in categories:
            for store in cat.get("stores", []):
                store_name = store.get("store_name", "")
                store_keywords = [k.lower() for k in store.get("keywords", [])]
                if any(kw in lowered_input for kw in store_keywords) or any(s.lower() in lowered_input for s in store_name.lower().split()):
                    for coupon in store.get("coupons", []):
                        found_coupons.append(f"🏷️ **المتجر:** {store_name}\n🔑 **الكود:** `{coupon.get('code')}`\n📝 **الوصف:** {coupon.get('description')}\n")

    if found_coupons:
        return "إليك الكوبونات والعروض المتاحة (من قاعدة المعرفة المحلية):\n\n" + "\n".join(found_coupons)
    
    return ""


# =========================================================
# 🤖 النظام الذكي الهجين (API أولاً ثم قاعدة المعرفة)
# =========================================================

def smart_process_request(user_input: str) -> tuple[str, str]:
    """
    يحاول الرد عبر الـ API أولاً. إذا حدث أي خطأ أو لم يتوفر مفتاح صالح،
    يتحول تلقائياً للبحث في قاعدة المعرفة والرد منها.
    """
    lowered = user_input.lower()
    coupon_keywords = ["عرض", "عروض", "كوبون", "كوبونات", "خصم", "تخفيض", "نون", "شي إن", "علي اكسبريس", "ملابس"]
    is_coupon_request = any(k in lowered for k in coupon_keywords)

    # 1. محاولة العمل عبر الـ API إذا كان المفتاح موجوداً وصحيحاً
    if PRIMARY_KEY and PRIMARY_KEY.startswith("AIza"):
        try:
            if is_coupon_request:
                prompt = (
                    f"بناءً على عروض وكوبونات التسوق لشبكة Saeed MarketAds، "
                    f"أجب بذكاء واحترافية على طلب العميل التالي: {user_input}"
                )
            else:
                prompt = f"أنت مساعد التسوق الذكي لشبكة Saeed MarketAds. رد بلباقة واحترافية باللغة العربية على: {user_input}"
            
            response = client_main.models.generate_content(model=MODEL_NAME, contents=prompt)
            if response and response.text:
                return response.text, "Gemini API 🚀"
        except Exception:
            pass  # في حال فشل الـ API، ينتقل مباشرة لقاعدة المعرفة أدناه

    # 2. التحويل التلقائي لقاعدة المعرفة المحلية (Fallback)
    if is_coupon_request:
        kb_result = search_knowledge_base(user_input)
        if kb_result:
            return kb_result, "قاعدة المعرفة المحلية (Knowledge Base) 📂"
        else:
            return "عذراً، لم أجد كوبوناً مطابهاً لطلبك في قاعدة المعرفة. انقر على زر (العروض الكبرى) للاطلاع على كافة التخفيضات.", "قاعدة المعرفة المحلية (Knowledge Base) 📂"
    else:
        # رد افتراضي ذكي من قاعدة المعرفة للدردشة العامة
        return f"أهلاً بك! أنا مساعد Saeed LogiC. أستقبل رسالتك '{user_input}' وجاهز لخدمتك وعرض أحدث الكوبونات والعروض.", "قاعدة المعرفة المحلية (Knowledge Base) 📂"


# =========================================================
# 🖥️ واجهة المستخدم (Streamlit UI)
# =========================================================

st.set_page_config(page_title="Saeed LogiC Pro", page_icon="🚀", layout="centered")
st.title("Saeed LogiC Pro 🚀")
st.subheader("النظام الذكي الهجين لإدارة العروض والتسويق")

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
        st.session_state.quick_action = "عروض نون وشي إن"


chat_input_val = st.chat_input("اسأل Saeed LogiC عن العروض، أو ألقِ التحية...")

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
        reply_text, source_used = smart_process_request(user_input)
        st.markdown(f"**[المصدر النشط: {source_used}]**")
        st.write(reply_text)

