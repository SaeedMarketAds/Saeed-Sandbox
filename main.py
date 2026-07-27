import streamlit as st
import json
import os
from datetime import datetime

# إعدادات صفحة التطبيق
st.set_page_config(
    page_title="Saeed LogiC Pro - مساعد التسوق الذكي",
    page_icon="🛍️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# تصميم وتنسيق الواجهة المظلمة الاحترافية (CSS)
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stTextInput input {
        background-color: #1a1c23;
        color: #ffffff;
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    .stButton button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton button:hover {
        opacity: 0.9;
        transform: scale(1.02);
    }
    .hero-box {
        padding: 20px;
        border-radius: 15px;
        background: linear-gradient(135deg, #1f2937 11.2%, #111827 91.1%);
        border: 1px solid #374151;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# واجهة الهيدر الترحيبية الاحترافية
st.markdown("""
    <div class="hero-box">
        <h1 style="color: #ffffff; margin-bottom: 5px;">Saeed LogiC Pro 🚀</h1>
        <p style="color: #9ca3af; font-size: 16px;">مساعد التسوق الذكي - محادثة حرة بلا حدود لتوفير الصفقات والعروض 🛍️</p>
    </div>
""", unsafe_allow_html=True)

# تحميل قاعدة المعرفة الخاصة بالعروض والمتاجر (نون، شي إن، علي إكسبريس)
@st.cache_data
def load_knowledge():
    if os.path.exists("data/knowledge.json"):
        with open("data/knowledge.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

knowledge_data = load_knowledge()

# أزرار الوصول السريع للمتاجر الكبرى (نون، شي إن، علي إكسبريس)
col1, col2, col3 = st.columns(3)
with col1:
    btn_noon = st.button("🔥 عروض نون")
with col2:
    btn_shein = st.button("👗 عروض شي إن")
with col3:
    btn_ali = st.button("🎯 علي إكسبريس")

# تهيئة سجل المحادثة الذكية
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "يا هلا فيك يا غالي في Saeed LogiC Pro! 🌟 أنا مساعدك الشخصي للتسوق والتوفير. ايش حاب تتسوق وتوفر اليوم؟ (جوال، ملابس، عروض نون أو شي إن أو علي إكسبريس)؟ أرسل لي اسم المنتج أو سعره وابشر باللي يسعدك!"}
    ]

# عرض رسائل المحادثة السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👨‍💻" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

# التعامل مع الأزرار السريعة
user_query = None
if btn_noon:
    user_query = "عروض نون"
elif btn_shein:
    user_query = "عروض شي إن"
elif btn_ali:
    user_query = "علي إكسبريس"
else:
    user_query = st.chat_input("عن أي شيء بلا حدود Saeed LogiC اكتب ما شئت.. اسأل أو اطلب عرضك...")

# منطق الرد الذكي والحواري الاستباقي
if user_query:
    # إضافة رسالة المستخدم للسجل
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user", avatar="👨‍💻"):
        st.markdown(user_query)

    # معالجة الرد الذكي بطريقة حوارية بشرية
    query_lower = user_query.lower()
    bot_response = ""

    if "السلام" in query_lower or "مرحبا" in query_lower or "اهلاً" in query_lower:
        bot_response = "وعليكم السلام ورحمة الله وبركاته يا هلا بيك يا الغالي! منور المنصة اليوم. ايش المنتج أو الجوال الذي في بالك ودك أبحث لك عن أرخص سعر وعرض له؟"
    elif "نون" in query_lower:
        bot_response = "🔥 **عروض وخزنة نون الحصرية المتاحة لك:**\n- **كود (NOON15):** خصم فوري بقيمة 15% على جميع المنتجات والأزياء.\n- **كود (NOON20):** خصم 20% على الطلبات الأولى للمستخدمين الجدد.\n\nهل تبحث عن منتج محدد في نون لأجلب لك سعره فوراً؟"
    elif "شي إن" in query_lower or "shein" in query_lower:
        bot_response = "👗 **عروض وتخفيضات شي إن الكبرى:**\n- **كود (SHEIN30):** خصم 30% على الفساتين والأزياء الصيفية الجديدة.\n- **كود (N73QS):** خصم 30% للمستخدمين الجدد على أول طلب.\n\nهل تريدني أن أبحث لك عن قطعة معينة أو ملابس بسعر مذهل؟"
    elif "علي" in query_lower or "aliexpress" in query_lower:
        bot_response = "🎯 **عروض علي إكسبريس (AliExpress):**\n- **كود (ALI50):** خصم يصل إلى 50% على الأجهزة الإلكترونية وإكسسوارات الهواتف.\n\nأرسل لي اسم الجوال أو المنتج الذي تبحث عنه وسأبحث لك عن أفضل صفقة! 🚀"
    elif "سعر" in query_lower or "جوال" in query_lower or "هاتف" in query_lower or "بكم" in query_lower:
        bot_response = "علا عينِي وراسي يا أبا رائد! 📱 يمديك ترسل لي اسم الجوال أو المنتج أو السعر الذي في بالك، وأنا أبحث لك في أقوى المتاجر وأعطيك العرض والكود حقه على طول بدون تعب!"
    else:
        # رد استباقي ذكي يحاوره بأسلوب تجاري احترافي
        bot_response = f"يا هلا بطلبك ('{user_query}'). بصفتي مساعدك الذكي، أنا جاهز أبحث لك عن أفضل الصفقات والكوبونات وتوفير أموالك. هل تحب أربط لك هذا الطلب مع عروض نون، شي إن، أو علي إكسبريس؟"

    # إضافة رد الروبوت للسجل وعرضه
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(bot_response)

# تذليل وتذييل الواجهة بحالة النظام وتاريخ التحديث
st.markdown("---")
col_status, col_time = st.columns(2)
with col_status:
    st.markdown("✅ **متصل وجاهز للعمل بكفاءة تامة**")
with col_time:
    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"📅 **آخر تحديث: {current_time_str}**")
