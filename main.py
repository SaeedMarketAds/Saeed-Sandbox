import streamlit as st
# 1. استيراد الدالة الذكية من محرك البحث
from engine.inference import search_knowledge_base

st.title("Saeed LogiC Pro 🚀")
st.subheader("نظام محلي لدمج العروض والكوبونات")

# ... (هنا يكون كود إعداد الجلسة session_state لحفظ المحادثة) ...

# 2. استقبال مدخلات المستخدم عبر الشات
if prompt := st.chat_input("اسألني عن العروض المتاحة..."):
    
    # عرض سؤال المستخدم في الواجهة
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # 3. اللمسة الذكية السحرية: استدعاء المحرك الحقيقي بدلاً من النص الثابت
    with st.chat_message("assistant"):
        with st.spinner("جاري فحص قاعدة المعرفة..."):
            
            # استدعاء الدالة وتمرير السؤال وملف البيانات
            # تأكد من كتابة المسار الصحيح لملف الـ json تبعاً لمجلد مشروعك
            bot_response = search_knowledge_base(prompt, json_path="conversation.json") 
            
            # عرض الإجابة الحقيقية للمستخدم
            st.markdown(bot_response)

    # ... (هنا يمكنك حفظ السؤال والإجابة في ملف conversation.json لتحديث السجل) ...
