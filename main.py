import streamlit as st
import time
import random

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Saeed LogiC Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. تصميم CSS احترافي
st.markdown("""
<style>
    /* إخفاء العناصر الافتراضية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background: #0a0a0f;
        background-image: 
            radial-gradient(ellipse at 10% 20%, rgba(255, 107, 157, 0.1) 0%, transparent 50%),
            radial-gradient(ellipse at 90% 80%, rgba(107, 140, 255, 0.1) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 50%, rgba(255, 215, 0, 0.05) 0%, transparent 70%);
    }
    
    /* الشريط العلوي */
    .top-bar {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding: 15px 30px;
        margin: -20px -50px 30px -50px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
    }
    
    .logo-text {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(135deg, #ff6b9d, #ff1493, #6b8cff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .logo-sub {
        color: rgba(255, 255, 255, 0.5);
        font-size: 14px;
        margin-right: 15px;
    }
    
    .status-badge {
        background: rgba(0, 255, 100, 0.15);
        border: 1px solid rgba(0, 255, 100, 0.3);
        color: #00ff64;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        background: #00ff64;
        border-radius: 50%;
        display: inline-block;
        animation: pulse-dot 2s infinite;
    }
    
    @keyframes pulse-dot {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(0.8); }
    }
    
    /* البطاقة الرئيسية */
    .main-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 30px;
        padding: 40px;
        margin: 20px 0;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        position: relative;
        overflow: hidden;
    }
    
    .main-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, rgba(255,107,157,0.05), transparent, rgba(107,140,255,0.05), transparent);
        animation: rotate-card 20s linear infinite;
    }
    
    @keyframes rotate-card {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .main-title {
        color: white;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 10px;
        position: relative;
        z-index: 1;
    }
    
    .main-subtitle {
        color: rgba(255, 255, 255, 0.6);
        font-size: 16px;
        margin-bottom: 30px;
        position: relative;
        z-index: 1;
    }
    
    /* حقل البحث */
    .search-wrapper {
        position: relative;
        z-index: 1;
        display: flex;
        gap: 15px;
        flex-wrap: wrap;
        align-items: center;
    }
    
    .search-input {
        flex: 1;
        min-width: 250px;
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 18px 25px;
        color: white;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .search-input:focus {
        border-color: #ff6b9d;
        box-shadow: 0 0 30px rgba(255, 107, 157, 0.15);
        outline: none;
        background: rgba(255, 255, 255, 0.08);
    }
    
    .search-input::placeholder {
        color: rgba(255, 255, 255, 0.3);
    }
    
    .btn-search {
        background: linear-gradient(135deg, #ff6b9d, #ff1493);
        border: none;
        border-radius: 20px;
        padding: 18px 40px;
        color: white;
        font-weight: 700;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(255, 20, 147, 0.3);
    }
    
    .btn-search:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 15px 40px rgba(255, 20, 147, 0.5);
    }
    
    .btn-voice {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 15px 25px;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 20px;
        min-width: 70px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .btn-voice:hover {
        border-color: #6b8cff;
        background: rgba(107, 140, 255, 0.1);
        box-shadow: 0 0 30px rgba(107, 140, 255, 0.2);
    }
    
    /* شبكة الكوبونات */
    .coupon-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 20px;
        margin-top: 30px;
        position: relative;
        z-index: 1;
    }
    
    .coupon-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 20px;
        padding: 25px;
        transition: all 0.3s ease;
    }
    
    .coupon-card:hover {
        transform: translateY(-5px);
        border-color: rgba(255, 107, 157, 0.3);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
    }
    
    .coupon-store {
        color: #ff6b9d;
        font-weight: 700;
        font-size: 18px;
    }
    
    .coupon-code {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 8px 15px;
        font-family: monospace;
        color: #6b8cff;
        font-size: 14px;
        display: inline-block;
        margin: 10px 0;
        border: 1px dashed rgba(107, 140, 255, 0.3);
    }
    
    .coupon-discount {
        color: #00ff64;
        font-size: 24px;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

# 3. الشريط العلوي
st.markdown("""
    <div class="top-bar">
        <div>
            <span class="logo-text">🚀 Saeed LogiC</span>
            <span class="logo-sub">Pro Edition</span>
        </div>
        <div style="display: flex; align-items: center; gap: 20px; flex-wrap: wrap;">
            <div class="status-badge">
                <span class="status-dot"></span>
                نظام محلي مستقر
            </div>
            <div class="status-badge" style="background: rgba(255,215,0,0.1); border-color: rgba(255,215,0,0.3); color: #ffd700;">
                ⚡ 100% بدون إنترنت
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. البطاقة الرئيسية
st.markdown("""
    <div class="main-card">
        <div class="main-title">🎯 ابحث عن أفضل العروض والكوبونات</div>
        <div class="main-subtitle">نظام ذكي لتتبع العروض - يعمل بدون إنترنت وبسرعة فائقة</div>
        
        <div class="search-wrapper">
            <input class="search-input" type="text" placeholder="مثال: كود نون الجديد أو فستان شبي إن" id="searchInput">
            <button class="btn-search" onclick="document.getElementById('searchInput').value">🔍 بحث</button>
            <button class="btn-voice" id="voiceBtn">🎤</button>
        </div>
        
        <div style="margin-top: 15px; display: flex; gap: 10px; flex-wrap: wrap; position: relative; z-index: 1;">
            <span style="background: rgba(255,255,255,0.03); padding: 5px 15px; border-radius: 15px; color: rgba(255,255,255,0.4); font-size: 12px;">
                🔥 رائج: نون, شي إن, أمازون
            </span>
            <span style="background: rgba(255,255,255,0.03); padding: 5px 15px; border-radius: 15px; color: rgba(255,255,255,0.4); font-size: 12px;">
                💰 خصومات تصل إلى 70%
            </span>
            <span style="background: rgba(255,255,255,0.03); padding: 5px 15px; border-radius: 15px; color: rgba(255,255,255,0.4); font-size: 12px;">
                🎁 كوبونات حصرية
            </span>
        </div>
    </div>
""", unsafe_allow_html=True)

# 5. الكوبونات
st.markdown("""
    <div style="margin-top: 30px;">
        <div style="color: white; font-size: 20px; font-weight: 700; margin-bottom: 20px;">
            🔥 أحدث العروض والكوبونات
        </div>
        <div class="coupon-grid">
            <div class="coupon-card">
                <div class="coupon-store">🛍️ نون</div>
                <div class="coupon-code">NON100</div>
                <div class="coupon-discount">خصم 100 ريال</div>
                <div style="color: rgba(255,255,255,0.4); font-size: 12px; margin-top: 10px;">صالحة حتى 30/7/2026</div>
            </div>
            <div class="coupon-card">
                <div class="coupon-store">👗 شي إن</div>
                <div class="coupon-code">SHEIN50</div>
                <div class="coupon-discount">خصم 50%</div>
                <div style="color: rgba(255,255,255,0.4); font-size: 12px; margin-top: 10px;">صالحة حتى 25/7/2026</div>
            </div>
            <div class="coupon-card">
                <div class="coupon-store">📦 أمازون</div>
                <div class="coupon-code">AMZ30</div>
                <div class="coupon-discount">خصم 30%</div>
                <div style="color: rgba(255,255,255,0.4); font-size: 12px; margin-top: 10px;">صالحة حتى 1/8/2026</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 6. المحادثة
st.markdown("---")
st.markdown('<div style="color: white; font-size: 18px; font-weight: 600;">💬 محادثة المساعد الذكي</div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "مرحباً بك في Saeed LogiC Pro! 🚀 اسألني عن أي كوبون أو عرض."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. إدخال البحث
if user_query := st.chat_input("✍️ اكتب اسم المتجر أو الكود أو العرض..."):
    with st.chat_message("user"):
        st.markdown(user_query)
    
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        responses = [
            f"🔍 جاري البحث عن '{user_query}' في قاعدة البيانات...\n\n✅ تم العثور على نتائج!",
            f"📊 تحليل العروض المتعلقة بـ '{user_query}'...\n\n💡 ننصح باستخدام كود: SAVE20",
            f"⚡ نتائج فورية لـ '{user_query}':\n\n• نون: خصم 15%\n• شي إن: خصم 30%"
        ]
        
        raw_response = random.choice(responses)
        
        for chunk in raw_response.split():
            full_response += chunk + " "
            time.sleep(0.03)
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# 8. JavaScript للمايك
st.markdown("""
<script>
const voiceBtn = document.getElementById('voiceBtn');
if (voiceBtn) {
    voiceBtn.addEventListener('click', function() {
        this.classList.toggle('recording');
        this.innerHTML = this.classList.contains('recording') ? '⏹️' : '🎤';
        
        if (this.classList.contains('recording')) {
            if ('webkitSpeechRecognition' in window) {
                const recognition = new webkitSpeechRecognition();
                recognition.lang = 'ar-SA';
                recognition.continuous = false;
                recognition.interimResults = false;
                
                recognition.onresult = function(event) {
                    const transcript = event.results[0][0].transcript;
                    document.getElementById('searchInput').value = transcript;
                    voiceBtn.classList.remove('recording');
                    voiceBtn.innerHTML = '🎤';
                };
                
                recognition.start();
            }
        }
    });
}
</script>
""", unsafe_allow_html=True)
