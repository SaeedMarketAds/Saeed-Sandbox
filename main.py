import streamlit as st
import os

# 1. تهيئة المجلدات تلقائياً في الخلفية لمنع أي أخطاء مسارات
os.makedirs("data", exist_ok=True)
os.makedirs("memory", exist_ok=True)

# 2. استيراد محرك الذكاء الاصطناعي مع معالجة الأخطاء
try:
    from inference import InferenceEngine
except ImportError as e:
    st.error(f"🚨 خطأ في استيراد ملف التشغيل (inference.py): {e}")
    st.stop()

# 3. تهيئة المحرك داخل ذاكرة الجلسة (session_state) لمنع خطأ AttributeError تماماً
if "engine" not in st.session_state:
    try:
        st.session_state.engine = InferenceEngine()
    except Exception as e:
        st.error(f"❌ فشل تشغيل محرك الذكاء الاصطناعي: {e}")
        st.stop()

# 4. تصميم واجهة التطبيق (متطابقة تماماً مع صورك الجميلة)
st.title("😀 Saeed Logic")
st.markdown("<h3 style='text-align: right;'>ذكاء اصطناعي محلي 100% — بدون API، بدون مفاتيح إنترنت</h3>", unsafe_html=True)
st.write("---")

# استقبال سؤال المستخدم عبر الحقل النصي
user_input = st.text_input("اطرح سؤالك هنا:", key="user_question_input")

if user_input:
    with st.spinner("جاري التفكير وتحليل الإجابة... ⏳"):
        try:
            # استدعاء الإجابة من المحرك المخزن بأمان داخل session_state
            response = st.session_state.engine.answer(user_input)
            
            # عرض الإجابة في صندوق أخضر جميل ومريح للعين
            st.success(response)
        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء معالجة السؤال: {e}")

st.write("---")

# 5. صندوق إضافة المعرفة (Expander) المتوافق مع واجهتك
with st.expander("➕ إضافة معرفة جديدة"):
    new_q = st.text_input("السؤال الجديد:")
    new_a = st.text_area("الإجابة المقترحة له:")
    
    if st.button("حفظ في الذاكرة 💾"):
        if new_q and new_a:
            success = st.session_state.engine.add_knowledge(new_q, new_a)
            if success:
                st.success("✅ تم حفظ المعلومة بنجاح في قاعدة بياناتك المحلية!")
                st.balloons() # تأثير بالونات احتفالي خفيف عند الحفظ بنجاح 🎉
            else:
                st.error("❌ حدث خطأ أثناء الحفظ، يرجى المحاولة مجدداً.")
        else:
            st.warning("⚠️ يرجى كتابة السؤال والإجابة أولاً قبل الضغط على حفظ.")

st.write("---")
st.markdown("<p style='text-align: center; color: #888;'>🚀 نظام ذكاء اصطناعي محلي يعمل بدون إنترنت</p>", unsafe_html=True)
