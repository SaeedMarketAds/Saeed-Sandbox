import streamlit as st
import time

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Saeed LogiC",
    page_icon="🛍️",
    layout="centered"
)

# 2. تصميم CSS لجعل المحادثة تبدو احترافية ومتناسقة باللغة العربية
st.markdown("""
    <style>
    .main .block-container {
        direction: RTL;
        text-align: right;
    }
    /* تنسيق صندوق الأفاتار */
    .avatar-container {
        text-align: center;
        padding: 10px;
        margin-bottom: 20px;
    }
    .avatar-img {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        border: 3px solid #00f2fe;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# 3. قسم الأفاتار المتكلم (مكانه في أعلى الواجهة ليقود المحادثة)
st.markdown('<div class="avatar-container">', unsafe_allow_html=True)
# يمكنك استبدال رابط الصورة برابط الأفاتار المتكلم الخاص بك (GIF أو فيديو أو رابط أداة مثل D-ID)
st.markdown('<img class="avatar-img" src="https://via.placeholder.com/150" alt="Saeed Avatar">', unsafe_allow_html=True)
st.markdown("<h3 style='color: #00f2fe; margin-top: 10px;'>مساعدك الذكي: Saeed LogiC</h3>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# 4. إدارة سجل المحادثة (عشان التطبيق يتذكر الأسئلة والأجوبة أثناء الجلسة)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "مرحباً بك! أنا مساعدك الذكي لتتبع الكوبونات والعروض. اسألني عن أي متجر أو كود تريد البحث عنه؟"}
    ]

# عرض الرسائل السابقة من السجل بتنسيق أنيق
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. خانة إدخال السؤال والجواب (تظهر أسفل الشاشة بشكل تلقائي وأنيق)
if user_query := st.chat_input("اسألني عن كوبون، متجر، أو عرض محدد..."):
    
    # عرض سؤال المستخدم فوراً في واجهة التشات
    with st.chat_message("user"):
        st.markdown(user_query)
    
    # حفظ سؤال المستخدم في السجل
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # هنا يتم استدعاء المحرك الخاص بك (Inference Engine) للبحث عن الإجابة
    # كمثال توضيحي سنضع استجابة محاكاة:
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # محاكاة كتابة الذكاء الاصطناعي خطوة بخطوة (تأثير ت typing)
        raw_response = f"جاري البحث عن '{user_query}' في قاعدة البيانات المحلية... للأسف لا توجد نتائج مطابقة حالياً، تأكد من تحديث ملف البيانات."
        
        for chunk in raw_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    # حفظ إجابة البوت في السجل
    st.session_state.messages.append({"role": "assistant", "content": full_response})

