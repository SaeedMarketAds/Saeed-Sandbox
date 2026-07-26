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

# محاولة جلب المفتاح من عدة مصادر
RAW_GEMINI_KEY = st.secrets.get("RAW_GEMINI_KEY", "")
BACKUP_API_KEY = st.secrets.get("BACKUP_API_KEY", "")
PRIMARY_KEY = RAW_GEMINI_KEY or BACKUP_API_KEY

# تهيئة العميل البرمجي
def initialize_client(api_key):
    try:
        if api_key and api_key.startswith("AIza"):
            return genai.Client(api_key=api_key)
        return None
    except Exception:
        return None

client_main = initialize_client(PRIMARY_KEY)

# =========================================================
# 📂 قاعدة المعرفة المحلية المتطورة (البديلة)
# =========================================================

def load_local_coupons():
    """تحميل قاعدة المعرفة الموسعة مع تحديثات ديناميكية"""
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
                    },
                    {
                        "store_name": "أمازون (Amazon)",
                        "keywords": ["أمازون", "amazon", "إلكترونيات", "كتب", "منتجات"],
                        "coupons": [
                            {"code": "AMZ20", "description": "خصم 20٪ على الكتب والقرطاسية."},
                            {"code": "AMZ15", "description": "خصم 15٪ على المنتجات المنزلية والإلكترونيات."}
                        ]
                    }
                ]
            },
            {
                "category_name": "المنزل والمطبخ",
                "stores": [
                    {
                        "store_name": "ساكو (Saco)",
                        "keywords": ["ساكو", "saco", "منزل", "مطبخ", "أثاث"],
                        "coupons": [
                            {"code": "SACO25", "description": "خصم 25٪ على أثاث المنزل والمطبخ."},
                            {"code": "SACO10", "description": "خصم 10٪ على أدوات المطبخ والكهربائيات."}
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
            "farewell": [
                "مع السلامة! 👋 نتمنى لك يوماً سعيداً وعروضاً مذهلة.",
                "شكراً لزيارتك! عوداً حميداً 🔄"
            ],
            "help": [
                "يمكنني مساعدتك في:\n✅ عرض الكوبونات والعروض\n✅ البحث عن خصومات حسب المتجر\n✅ تقديم نصائح التسوق الذكية\n📝 فقط اسألني عن أي متجر أو منتج!"
            ]
        }
    }

def search_knowledge_base(user_input: str) -> dict:
    """البحث المتقدم في قاعدة المعرفة مع نتائج مرتبة"""
    knowledge_data = load_local_coupons()
    lowered_input = user_input.lower().strip()
    
    results = {
        "coupons": [],
        "greeting_response": None,
        "help_response": None,
        "farewell_response": None
    }
    
    # التحقق من التحية
    greeting_keywords = ["السلام", "مرحب", "اهلا", "هلا", "سلام"]
    if any(k in lowered_input for k in greeting_keywords):
        results["greeting_response"] = random.choice(knowledge_data["responses"]["greetings"])
        return results
    
    # التحقق من الوداع
    farewell_keywords = ["مع السلامة", "وداع", "باي", "bye"]
    if any(k in lowered_input for k in farewell_keywords):
        results["farewell_response"] = random.choice(knowledge_data["responses"]["farewell"])
        return results
    
    # التحقق من طلب المساعدة
    help_keywords = ["مساعدة", "help", "كيف", "طريقة"]
    if any(k in lowered_input for k in help_keywords):
        results["help_response"] = "\n".join(knowledge_data["responses"]["help"])
        return results
    
    # البحث عن الكوبونات
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
        # بحث محدد حسب المتجر
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
    
    # ترتيب النتائج حسب الصلة
    results["coupons"].sort(key=lambda x: x["relevance"], reverse=True)
    return results

def format_knowledge_response(results: dict) -> str:
    """تنسيق نتائج قاعدة المعرفة بشكل احترافي"""
    if results.get("greeting_response"):
        return results["greeting_response"]
    
    if results.get("farewell_response"):
        return results["farewell_response"]
    
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
    
    return "🔍 لم أجد كوبونات مطابقة لبحثك. جرب البحث عن متجر محدد مثل 'نون' أو 'شي إن'."

# =========================================================
# 🤖 النظام الذكي الهجين المطور
# =========================================================

def smart_process_request(user_input: str) -> tuple[str, str]:
    """نظام ذكي هجين يعطي أولوية للـ API مع تحويل ذكي لقاعدة المعرفة"""
    
    # 1. محاولة العمل عبر الـ API
    if client_main and PRIMARY_KEY and PRIMARY_KEY.startswith("AIza"):
        try:
            # بناء برومبت ديناميكي ذكي
            system_prompt = """أنت مساعد تسوق ذكي متخصص في العروض والكوبونات. 
            لديك معرفة واسعة بأسواق التسوق الإلكتروني في السعودية.
            تحدث باللغة العربية الفصحى مع لمسة عربية ودية.
            كن مفيداً، دقيقاً، وتفاعلياً."""
            
            user_prompt = f"""رد على استفسار العميل التالي بطريقة احترافية وذكية:
            {user_input}
            
            إذا كان الطلب عن عروض أو كوبونات، قدم تفاصيل دقيقة.
            إذا كان سؤالاً عاماً، رد بلباقة واحترافية."""
            
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            response = client_main.models.generate_content(
                model=MODEL_NAME,
                contents=full_prompt
            )
            
            if response and response.text:
                return response.text, "Gemini API 🚀"
        except Exception as e:
            # سجل الخطأ للتصحيح
            pass
    
    # 2. التحويل الذكي لقاعدة المعرفة
    kb_results = search_knowledge_base(user_input)
    formatted_response = format_knowledge_response(kb_results)
    
    # إذا كانت النتيجة فارغة، استخدم ردوداً ذكية افتراضية
    if not formatted_response or formatted_response == "🔍 لم أجد كوبونات مطابقة لبحثك. جرب البحث عن متجر محدد مثل 'نون' أو 'شي إن'.":
        # تحقق من كلمات مفتاحية معينة
        if any(w in user_input.lower() for w in ["نون", "noon"]):
            formatted_response = "🛍️ **عروض نون:**\n\n🏷️ خصم 15٪ على جميع المنتجات (كود: NOON15)\n🏷️ خصم 20٪ للطلبات الأولى (كود: NOON20)\n🏷️ خصم 10٪ على الإلكترونيات (كود: NOON10)"
        elif any(w in user_input.lower() for w in ["شي إن", "shein", "شي ان"]):
            formatted_response = "👗 **عروض شي إن:**\n\n🏷️ خصم 30٪ على الفساتين الجديدة (كود: SHEIN30)\n🏷️ خصم 30٪ للمستخدمين الجدد (كود: N73QS)\n🏷️ خصم 15٪ للطلبات فوق 100 ريال (كود: SHEIN15)"
        else:
            formatted_response = "🎯 **مرحباً بك في سوق العروض!**\n\nيمكنني مساعدتك في:\n✅ عرض كوبونات نون\n✅ عروض شي إن\n✅ خصومات الإلكترونيات\n📝 فقط أخبرني ما المتجر الذي تبحث عنه؟"
    
    return formatted_response, "قاعدة المعرفة المحلية 📂"

# =========================================================
# 🖥️ واجهة المستخدم المتطورة
# =========================================================

st.set_page_config(
    page_title="Saeed LogiC Pro - مساعد التسوق الذكي",
    page_icon="🛍️",
    layout="wide"
)

# تخصيص CSS
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
    .offer-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    .coupon-code {
        background: #e9ecef;
        padding: 0.25rem 0.75rem;
        border-radius: 5px;
        font-family: monospace;
        font-weight: bold;
        color: #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown(f"""
<div class="main-header">
    <h1>🛍️ Saeed LogiC Pro</h1>
    <p>🚀 مساعد التسوق الذكي - أحدث العروض والكوبونات</p>
    <small>✨ نظام ذكي هجين يعمل بالـ API وقاعدة المعرفة المحلية</small>
</div>
""", unsafe_allow_html=True)

# الأزرار السريعة
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

# منطقة الدردشة
st.markdown("---")
st.markdown("### 💬 **تحدث مع مساعد التسوق الذكي**")

# حالة النظام
status_col1, status_col2 = st.columns(2)
with status_col1:
    if PRIMARY_KEY and PRIMARY_KEY.startswith("AIza"):
        st.success("✅ الـ API متصل وجاهز للعمل")
    else:
        st.warning("⚠️ يعمل من قاعدة المعرفة المحلية")

with status_col2:
    st.info(f"📅 آخر تحديث: {load_local_coupons()['metadata']['last_update']}")

# معالجة المدخلات
chat_input_val = st.chat_input("اسأل Saeed LogiC عن العروض، أو ألقِ التحية...")

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
        with st.spinner("🤔 جاري التفكير..."):
            reply_text, source_used = smart_process_request(user_input)
        
        # عرض مصدر الرد
        if "Gemini API" in source_used:
            st.success(f"💡 {source_used}")
        else:
            st.info(f"📚 {source_used}")
        
        # عرض الرد بشكل منسق
        st.markdown(reply_text)

# تذييل الصفحة
st.markdown("---")
st.caption("""
**Saeed LogiC Pro v2.0** | نظام ذكي هجين 
🤖 يعمل بالـ Gemini API مع تحويل آلي لقاعدة المعرفة المحلية
""")
