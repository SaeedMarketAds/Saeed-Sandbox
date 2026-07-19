import streamlit as st

# 1. إعدادات الصفحة الأساسية لتظهر بشكل ممتد ومناسب للهواتف والمتصفح
st.set_page_config(
    page_title="Saeed LogiC",
    page_icon="🛍️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. إضافة لمسات CSS مخصصة لجعل الواجهة أنيقة واحترافية
st.markdown("""
    <style>
    /* تنسيق اتجاه النصوص ليدعم اللغة العربية بشكل كامل */
    .main .block-container {
        direction: RTL;
        text-align: right;
    }
    
    /* تصميم كروت الكوبونات الاحترافية */
    .coupon-card {
        background-color: #1e293b; /* لون خلفية داكن وأنيق */
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid #334155;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    
    /* تأثير خفيف عند تمرير الماوس أو الضغط على الكارت */
    .coupon-card:hover {
        transform: translateY(-3px);
        border-color: #00f2fe; /* لون إضاءة مميز */
    }
    
    /* تنسيق اسم المتجر داخل الكارت */
    .store-name {
        font-size: 20px;
        font-weight: bold;
        color: #00f2fe;
        margin-bottom: 8px;
    }
    
    /* تنسيق كود الكوبون ليكون بارزاً وسهل النسخ */
    .coupon-code-box {
        background: linear-gradient(135deg, #0072ff, #00f2fe);
        color: #ffffff;
        padding: 6px 16px;
        border-radius: 8px;
        font-weight: bold;
        font-family: 'Courier New', Courier, monospace;
        display: inline-block;
        letter-spacing: 1px;
    }
    
    /* تنسيق روابط المتاجر */
    .store-link {
        color: #94a3b8;
        text-decoration: none;
        font-size: 14px;
        transition: color 0.2s;
    }
    .store-link:hover {
        color: #00f2fe;
    }
    </style>
""", unsafe_allow_html=True)

# 3. الهيدر الرئيسي للتطبيق
st.markdown("<h1 style='text-align: center; color: #00f2fe; margin-bottom: 5px;'>🛍️ Saeed LogiC</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 16px;'>مساعد التسوق المحلي المستقر لتتبع العروض والكوبونات - 100% بدون إنترنت</p>", unsafe_allow_html=True)
st.markdown("---")

# 4. قسم البحث الذكي
st.markdown("### 🔍 ابحث عن متجر، كود، أو عرض محدد")
search_query = st.text_input("", placeholder="اكتب اسم المتجر أو الكود هنا (مثال: AliExpress، Noon)...", label_visibility="collapsed")

# أزرار البحث بتنسيق متناسق
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    search_btn = st.button("🚀 ابدأ البحث الذكي", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# 5. عرض النتائج (مثال توضيحي لكيفية ظهور الكوبونات بالأناقة الجديدة)
st.markdown("### ✨ آخر العروض والكوبونات المتاحة")

# بيانات تجريبية لمحاكاة الشكل النهائي (ستربطها لاحقاً بملف knowledge.json)
sample_data = [
    {"store": "AliExpress", "code": "ALI50", "desc": "خصم يصل إلى 50% على الأجهزة الإلكترونية المختارة.", "link": "#"},
    {"store": "SHEIN", "code": "FASHION20", "desc": "خصم إضافي 20% على تشكيلة الملابس الصيفية.", "link": "#"},
    {"store": "Noon", "code": "NOON99", "desc": "شحن مجاني + خصم 10% على الطلبات فوق 200 ريال.", "link": "#"}
]

# حلقة تكرارية لعرض الكروت بناءً على البيانات
for item in sample_data:
    st.markdown(f"""
        <div class="coupon-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div class="store-name">🏪 {item['store']}</div>
                <div><a class="store-link" href="{item['link']}" target="_blank">🔗 زيارة المتجر</a></div>
            </div>
            <p style="color: #cbd5e1; margin: 10px 0 15px 0; font-size: 15px;">🎁 {item['desc']}</p>
            <div style="display: flex; justify-content: space-between; align-items: center; direction: ltr;">
                <span class="coupon-code-box">{item['code']}</span>
                <span style="color: #64748b; font-size: 12px; direction: rtl;">⚡ كود فعال</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
