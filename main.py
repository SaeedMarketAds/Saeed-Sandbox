import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)

import json
import os
import re
import streamlit as st
from google import genai
from datetime import datetime
import random

# =========================================================
# 🔑 إعدادات الموديل والمفاتيح
# =========================================================

MODEL_NAME = "gemini-1.5-flash"

RAW_GEMINI_KEY = st.secrets.get("RAW_GEMINI_KEY", "")
BACKUP_API_KEY = st.secrets.get("BACKUP_API_KEY", "")
PRIMARY_KEY = RAW_GEMINI_KEY or BACKUP_API_KEY

def initialize_client(api_key):
    try:
        if api_key and api_key.startswith("AIza"):
            return genai.Client(api_key=api_key)
        return None
    except Exception:
        return None

client_main = initialize_client(PRIMARY_KEY)

# =========================================================
# 📂 قاعدة المعرفة المحلية (البديلة)
# =========================================================

def load_local_coupons():
    return {
        "metadata": {
            "platform_name": "Saeed MarketAds",
            "bot_name": "Saeed LogiC Pro",
            "version": "2.0",
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "categories": [
            {
                "category_name": "تسوق عام وأزياء",
                "stores": [
                    {
                        "store_name": "نون (Noon)",
                        "keywords": ["نون", "noon", "خصم", "عروض", "كود", "تخفيض"],
                        "coupons": [
                            {"code": "NOON15", "description": "خصم فوري بقيمة 15٪ على جميع المنتجات والملابس."},
                            {"code": "NOON20", "description": "خصم 20٪ على الطلبات الأولى للمستخدمين الجدد."},
                            {"code": "NOON10", "description": "خصم 10٪ على الأجهزة الإلكترونية والإكسسوارات."}
                        ]
                    },
                    {
                        "store_name": "شي إن (SHEIN)",
                        "keywords": ["شي إن", "shein", "ملابس", "فساتين", "شي ان", "ازياء"],
                        "coupons": [
                            {"code": "SHEIN30", "description": "خصم 30٪ على الفساتين والملابس الصيفية الجديدة."},
                            {"code": "N73QS", "description": "خصم 30% للمستخدمين الجدد، يربط المتسوق بمختاراتك الخاصة."},
                            {"code": "SHEIN15", "description": "خصم 15٪ على كل الطلبات التي تزيد عن 100 ريال."}
                        ]
                    }
                ]
            },
            {
                "category_name": "الإلكترونيات والتقنية",
                "stores": [
                    {
                        "store_name": "علي إكسبريس (AliExpress)",
                        "keywords": ["علي إكسبريس", "aliexpress", "علي اكسبريس", "إلكترونيات", "تقنية"],
                        "coupons": [
                            {"code": "ALI50", "description": "خصم يصل إلى 50٪ على الأجهزة الإلكترونية وإكسسوارات الهواتف."},
                            {"code": "ALI25", "description": "خصم 25٪ على الهواتف الذكية والأجهزة اللوحية."}
                        ]
                    }
                ]
            }
        ],
        "responses": {
            "greetings": [
                "أهلاً وسهلاً بك! 🌟 كيف يمكنني مساعدتك اليوم؟",
                "مرحباً! أنا سعيد بخدمتك. هل تبحث عن عروض أو كوبونات؟ 💰",
                "السلام عليكم! 👋 أنا مساعد التسوق الذكي، جاهز لعرض أحدث العروض."
            ],
            "help": [
                "يمكنني مساعدتك في:\n✅ عرض الكوبونات والعروض\n✅ البحث عن خصومات حسب المتجر\n✅ الإجابة على أي استفسارات أو مواضيع بلا حدود\n📝 فقط اسألني عما تريد!"
            ]
        }
    }

def search_knowledge_base(user_input: str) -> dict:
    knowledge_data = load_local_coupons()
    lowered_input = user_input.lower().strip()
    
    results = {
        "coupons": [],
        "greeting_response": None,
        "help_response": None
    }
    
    greeting_keywords = ["السلام", "مرحب", "اهلا", "هلا", "سلام", "hi", "hello"]
    if any(k in lowered_input for k in greeting_keywords):
        results["greeting_response"] = random.choice(knowledge_data["responses"]["greetings"])
        return results
    
    help_keywords = ["مساعدة", "help", "كيف", "طريقة", "من انت"]
    if any(k in lowered_input for k in help_keywords):
        results["help_response"] = "\n".join(knowledge_data["responses"]["help"])
        return results
    
    if any(w in lowered_input for w in ["عرض", "عروض", "كوبون", "كوبونات", "خصم", "تخفيض", "كل"]):
        for cat in knowledge_data.get("categories", []):
            for store in cat.get("stores", []):
                for coupon in store.get("coupons", []):
                    results["coupons"].append({
                        "store": store.get("store_name"),
                        "code": coupon.get("code"),
                        "description": coupon.get("description"),
                        "category": cat.get("category_name"),
                        "relevance": 1.0
                    })
    else:
        for cat in knowledge_data.get("categories", []):
            for store in cat.get("stores", []):
                store_name = store.get("store_name", "")
                store_keywords = [k.lower() for k in store.get("keywords", [])]
                
                relevance = 0
                if any(kw in lowered_input for kw in store_keywords):
                    relevance += 2
                if any(s.lower() in lowered_input for s in store_name.lower().split()):
                    relevance += 1
                
                if relevance > 0:
                    for coupon in store.get("coupons", []):
                        results["coupons"].append({
                            "store": store_name,
                            "code": coupon.get("code"),
                            "description": coupon.get("description"),
                            "category": cat.get("category_name"),
                            "relevance": relevance
                        })
    
    results["coupons"].sort(key=lambda x: x["relevance"], reverse=True)
    return results

def format_knowledge_response(results: dict) -> str:
    if results.get("greeting_response"):
        return results["greeting_response"]
    if results.get("help_response"):
        return results["help_response"]
    if results["coupons"]:
        response = "🎯 **أحدث العروض والكوبونات المتاحة:**\n\n"
        current_category = None
        for coupon in results["coupons"]:
            if coupon["category"] != current_category:
                current_category = coupon["category"]
                response += f"📂 **{current_category}**\n"
            response += f"🏷️ **{coupon['store']}**\n"
            response += f"🔑 **الكود:** `{coupon['code']}`\n"
            response += f"📝 **الوصف:** {coupon['description']}\n\n"
        return response
    return ""

# =========================================================
# 🤖 النظام الذكي الهجين (API حر بلا حدود)
# =========================================================

def smart_process_request(user_input: str) -> tuple[str, str]:
    # 1. المحاولة عبر الـ API بدون قيود على طول النص أو الموضوع
    if client_main and PRIMARY_KEY and PRIMARY_KEY.startswith("AIza"):
        try:
            system_prompt = (
                "أنت مساعد تسوق ذكي ومستشار رقمي لشبكة Saeed MarketAds. "
                "أجب على المستخدم بكل حرية وبدون أي قيود أو حدود على حجم الإجابة أو مواضيعها. "
                "تحدث بلغة عربية فصحى واضحة وودية."
            )
            full_prompt = f"{system_prompt}\n\nسؤال أو طلب المستخدم:\n{user_input}"
            
            response = client_main.models.generate_content(
                model=MODEL_NAME,
                contents=full_prompt
            )
            
            if response and response.text:
                return response.text, "Gemini API 🚀"
        except Exception:
            pass
    
    # 2. التحويل التلقائي لقاعدة المعرفة المحلية عند تعذر الـ API
    kb_results = search_knowledge_base(user_input)
    formatted_response = format_knowledge_response(kb_results)
    
    if formatted_response:
        return formatted_response, "قاعدة المعرفة المحلية 📂"
    
    # إذا لم يطابق بحثاً محدداً في قاعدة المعرفة، يتم إعطاء النص كاملاً كمساعد افتراضي حر
    return f"أهلاً بك! لقد استلمت رسالتك: '{user_input}'. أنا جاهز تماماً للرد ومساعدتك في أي استفسار تسوقي أو تقني بلا حدود.", "قاعدة المعرفة المحلية 📂"

# =========================================================
# 🖥️ واجهة المستخدم (Streamlit UI)
# =========================================================

st.set_page_config(
    page_title="Saeed LogiC Pro - مساعد التسوق الذكي",
    page_icon="🛍️",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🛍️ Saeed LogiC Pro</h1>
    <p>🚀 مساعد التسوق الذكي - محادثة حرة بلا حدود</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📋 العروض الكبرى", use_container_width=True):
        knowledge_data = load_local_coupons()
        st.success("🎉 **جميع العروض والكوبونات المتاحة:**")
        for cat in knowledge_data.get("categories", []):
            st.markdown(f"### 📂 {cat.get('category_name')}")
            for store in cat.get("stores", []):
                st.markdown(f"**{store.get('store_name')}**")
                for coupon in store.get("coupons", []):
                    st.code(coupon.get('code'), language="text")
                    st.write(coupon.get('description'))
                st.divider()

with col2:
    if st.button("🔥 عروض نون", use_container_width=True):
        st.session_state.quick_action = "نون"

with col3:
    if st.button("👗 عروض شي إن", use_container_width=True):
        st.session_state.quick_action = "شي إن"

st.markdown("---")

status_col1, status_col2 = st.columns(2)
with status_col1:
    if PRIMARY_KEY and PRIMARY_KEY.startswith("AIza"):
        st.success("✅ الـ API متصل وجاهز للعمل بلا حدود")
    else:
        st.warning("⚠️ يعمل من قاعدة المعرفة المحلية")

with status_col2:
    st.info(f"📅 آخر تحديث: {load_local_coupons()['metadata']['last_update']}")

chat_input_val = st.chat_input("اكتب ما شئت.. اسأل Saeed LogiC عن أي شيء بلا حدود...")

user_input = None
if chat_input_val:
    user_input = chat_input_val
elif hasattr(st.session_state, 'quick_action') and st.session_state.quick_action:
    user_input = st.session_state.quick_action
    st.session_state.quick_action = None

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
        
    with st.chat_message("assistant"):
        with st.spinner("🤔 جاري التفكير والرد..."):
            reply_text, source_used = smart_process_request(user_input)
        
        if "Gemini API" in source_used:
            st.success(f"💡 {source_used}")
        else:
            st.info(f"📚 {source_used}")
        
        st.markdown(reply_text)

