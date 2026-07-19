import streamlit as st
import time
import random

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Saeed LogiC - المساعد الرومانسي",
    page_icon="🌙",
    layout="wide"
)

# 2. تصميم CSS رومانسي وجذاب
st.markdown("""
    <style>
    /* خلفية رومانسية مع تدرج ألوان */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    .main .block-container {
        direction: RTL;
        text-align: center;
        padding-top: 2rem;
    }
    
    /* تنسيق الأفاتار الرومانسي */
    .avatar-container {
        position: relative;
        text-align: center;
        padding: 20px;
        margin: 20px auto;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 30px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 182, 193, 0.3);
        box-shadow: 0 0 50px rgba(255, 105, 180, 0.2);
        max-width: 500px;
    }
    
    .avatar-img {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        border: 4px solid #ff6b9d;
        box-shadow: 0 0 30px rgba(255, 107, 157, 0.5);
        transition: all 0.5s ease;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 0 20px #ff6b9d; }
        to { box-shadow: 0 0 50px #ff1493, 0 0 100px #ff6b9d; }
    }
    
    .avatar-img:hover {
        transform: scale(1.05) rotate(-5deg);
    }
    
    .name-title {
        color: #ff6b9d;
        font-size: 28px;
        font-weight: bold;
        margin-top: 10px;
        text-shadow: 0 0 20px rgba(255, 107, 157, 0.5);
        font-family: 'Amiri', 'Arial', sans-serif;
    }
    
    .sub-title {
        color: #ffb6c1;
        font-size: 16px;
        opacity: 0.8;
        font-style: italic;
    }
    
    /* تنسيق الأزرار الرومانسية */
    .romantic-btn {
        background: linear-gradient(135deg, #ff6b9d, #ff1493);
        border: none;
        color: white;
        padding: 12px 35px;
        border-radius: 50px;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 25px rgba(255, 20, 147, 0.4);
        margin: 10px 5px;
        font-family: 'Amiri', 'Arial', sans-serif;
    }
    
    .romantic-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 35px rgba(255, 20, 147, 0.6);
        background: linear-gradient(135deg, #ff1493, #ff6b9d);
    }
    
    .romantic-btn-secondary {
        background: linear-gradient(135deg, #6b8cff, #4a6cf7);
        border: none;
        color: white;
        padding: 12px 35px;
        border-radius: 50px;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 25px rgba(74, 108, 247, 0.4);
        margin: 10px 5px;
        font-family: 'Amiri', 'Arial', sans-serif;
    }
    
    .romantic-btn-secondary:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 35px rgba(74, 108, 247, 0.6);
    }
    
    /* تنسيق مربع المايك */
    .mic-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 30px;
        padding: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 182, 193, 0.2);
        margin: 20px 0;
        display: inline-block;
    }
    
    .mic-btn {
        background: linear-gradient(135deg, #ff6b9d, #ff1493);
        border: none;
        border-radius: 50%;
        width: 80px;
        height: 80px;
        color: white;
        font-size: 35px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 0 30px rgba(255, 20, 147, 0.4);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 20px rgba(255, 20, 147, 0.4); }
        50% { box-shadow: 0 0 50px rgba(255, 20, 147, 0.8), 0 0 80px rgba(255, 20, 147, 0.4); }
        100% { box-shadow: 0 0 20px rgba(255, 20, 147, 0.4); }
    }
    
    .mic-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 0 60px rgba(255, 20, 147, 0.8);
    }
    
    /* تنسيق رسائل المحادثة */
    .chat-message {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 15px 25px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 182, 193, 0.1);
    }
    
    .user-message {
        background: rgba(255, 107, 157, 0.15);
        border-right: 3px solid #ff6b9d;
    }
    
    .assistant-message {
        background: rgba(107, 140, 255, 0.15);
        border-right: 3px solid #6b8cff;
    }
    
    /* تنسيق مربع الإدخال */
    .search-box {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(255, 182, 193, 0.3);
        border-radius: 50px;
        padding: 15px 25px;
        color: white;
        font-size: 18px;
        width: 100%;
        max-width: 600px;
        margin: 10px auto;
        backdrop-filter: blur(10px);
    }
    
    .search-box:focus {
        border-color: #ff6b9d;
        box-shadow: 0 0 30px rgba(255, 107, 157, 0.3);
        outline: none;
    }
    
    /* نصوص متحركة */
    .floating-hearts {
        position: fixed;
        pointer-events: none;
        font-size: 24px;
        animation: floatUp 4s ease-in infinite;
    }
    
    @keyframes floatUp {
        0% { opacity: 1; transform: translateY(0) scale(1); }
        100% { opacity: 0; transform: translateY(-200px) scale(0.5); }
    }
    </style>
""", unsafe_allow_html=True)

# 3. عرض الورود المتطايرة (تأثير رومانسي)
hearts = ['❤️', '🌸', '🌹', '💖', '✨', '🌺']
for i in range(6):
    st.markdown(f"""
        <div class="floating-hearts" style="left: {random.randint(5, 95)}%; animation-delay: {i * 0.5}s;">
            {random.choice(hearts)}
        </div>
    """, unsafe_allow_html=True)

# 4. الأفاتار الرومانسي
st.markdown("""
    <div class="avatar-container">
        <img class="avatar-img" src="https://i.pinimg.com/736x/9e/5b/0b/9e5b0b8e12e5e4f2a1a5c7d3f8b6a9e2.jpg" alt="Saeed Avatar">
        <div class="name-title">💫 Saeed LogiC 💫</div>
        <div class="sub-title">✨ مساعدك الذكي لعالم التوفير ✨</div>
        <div style="color: #ffb6c1; font-size: 14px; margin-top: 10px;">
            💝 أحلى العروض بلمسة رومانسية 💝
        </div>
    </div>
""", unsafe_allow_html=True)

# 5. الأزرار الرومانسية
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
        <button class="romantic-btn">🛍️ عروض اليوم</button>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
        <button class="romantic-btn-secondary">💝 كوبونات حصرية</button>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
        <button class="romantic-btn">🌟 متاجر مميزة</button>
    """, unsafe_allow_html=True)

st.markdown("---")

# 6. إدارة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "🌹 أهلاً بك في عالم التوفير الرومانسي! كيف يمكنني مساعدتك اليوم؟ 💝"}
    ]

# عرض الرسائل بتنسيق رومانسي
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.markdown(f"💫 {message['content']}")
        else:
            st.markdown(f"💝 {message['content']}")

# 7. مربع المايك والبحث
col1, col2 = st.columns([5, 1])

with col1:
    if user_query := st.chat_input("💭 اكتب سؤالك هنا... (مثال: كود نون الجديد)"):
        with st.chat_message("user"):
            st.markdown(f"💝 {user_query}")
        
        st.session_state.messages.append({"role": "user", "content": user_query})
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # محاكاة استجابة رومانسية
            romantic_responses = [
                f"🌹 بحثت عن '{user_query}' في قاعدة بيانات الحب والتوفير...",
                f"💖 وجدت لك عروضاً رائعة! لكن دعني أبحث بشكل أعمق...",
                f"✨ عذراً يا جميل، لم أجد ما تبحث عنه حالياً، لكن ثق بي سأجد لك أفضل العروض! 💝"
            ]
            
            raw_response = random.choice(romantic_responses)
            
            for chunk in raw_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(f"💫 {full_response}▌")
            
            message_placeholder.markdown(f"💫 {full_response}")
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})

with col2:
    st.markdown("""
        <div style="text-align: center; padding: 10px;">
            <button class="mic-btn" title="اضغط للتحدث">
                🎤
            </button>
            <div style="color: #ffb6c1; font-size: 12px; margin-top: 5px;">
                تحدث بصوتك
            </div>
        </div>
    """, unsafe_allow_html=True)

# 8. نصائح رومانسية في الأسفل
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #ffb6c1; padding: 20px; background: rgba(255,255,255,0.05); border-radius: 20px; backdrop-filter: blur(10px);">
        🌟 <strong>نصائح التوفير الرومانسية</strong> 🌟<br>
        💝 استخدم كود "ROMANTIC10" للحصول على خصم 10%<br>
        🌹 تابع عروض عيد الحب والحفلات الرومانسية<br>
        ✨ شاركنا تجربتك وسنقدم لك هدايا مميزة
    </div>
""", unsafe_allow_html=True)
