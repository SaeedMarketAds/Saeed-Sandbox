import streamlit as st
import os

# ====================================================
# القسم 1: تهيئة المجلدات وإعدادات الصفحة الأساسية
# ====================================================

# تهيئة المجلدات تلقائياً في الخلفية
os.makedirs("data", exist_ok=True)
os.makedirs("memory", exist_ok=True)

# إعداد الصفحة بالاسم المعتمد والوجه الضاحك الفخم 😀
# (ملاحظة برمجية: يجب أن يكون هذا الأمر هو أول أمر من أوامر Streamlit في الملف)
st.set_page_config(page_title="Saeed Logic", page_icon="😀", layout="centered")


# ====================================================
# القسم 2: استيراد محرك الذكاء الاصطناعي وتشغيله
# ====================================================

# استيراد محرك الذكاء الاصطناعي مع معالجة أخطاء الاستيراد
try:
    from inference import InferenceEngine
except ImportError as e:
    st.error(f"🚨 خطأ في استيراد ملف التشغيل (inference.py): {e}")
    st.stop()

# تهيئة المحرك داخل ذاكرة الجلسة بأمان
if "engine" not in st.session_state:
    try:
        st.session_state.engine = InferenceEngine()
    except Exception as e:
        st.error(f"❌ فشل تشغيل محرك الذكاء الاصطناعي: {e}")
        st.stop()


# ====================================================
# القسم 3: تصميم الواجهة العلوية والترحيب الذكي بالزبائن
# ====================================================

st.markdown("<h1 style='text-align: right;'>😀 Saeed Logic</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: right; color: #888;'>ذكاء اصطناعي محلي 100% — بدون API، بدون مفاتيح إنترنت</h4>", unsafe_allow_html=True)
st.write("---")

# كود استقبال اسم الزبون للترحيب به بشكل مؤقت وآمن
user_name = st.text_input("مرحباً بك في Saeed LogiC! يرجى كتابة اسمك لنبدأ:", placeholder="اكتب اسمك هنا...")

if user_name:
    st.success(f"👋 أهلاً بك يا **{user_name}**، كيف يمكنني مساعدتك اليوم في سعيد ماركت؟")
else:
    st.info("💡 يرجى كتابة اسمك في الخانة أعلاه ليخاطبك البوت باسمك الشخصي.")

st.write("---")


# ====================================================
# القسم 4: استقبال سؤال المستخدم ومعالجته بالذكاء الاصطناعي
# ====================================================

# تخصيص نص السؤال ليتفاعل مع اسم الزبون إذا كُتب
input_label = f"اطرح سؤالك هنا يا {user_name}:" if user_name else "اطرح سؤالك هنا:"
user_input = st.text_input(input_label, placeholder="اكتب سؤالك هنا...", key="user_question")

if user_input:
    with st.spinner("جاري التفكير وتحليل الإجابة... ⏳"):
        try:
            # التحقق الوقائي من وجود دالة الاستجابة لتجنب الانهيار
            if hasattr(st.session_state.engine, "answer"):
                response = st.session_state.engine.answer(user_input)
                st.success(response)
            else:
                st.error("❌ خطأ برمجي: دالة الاستجابة (answer) غير معرّفة بالشكل الصحيح داخل ملف inference.py")
        except AttributeError as ae:
            st.error(f"⚠️ تنبيه خصائص (AttributeError): {ae}")
            st.info("يوجد نقص أو خطأ إملائي في تعريف المتغيرات البرمجية داخل ملف inference.py الخاص بك.")
        except Exception as e:
            st.error(f"❌ حدث خطأ غير متوقع: {e}")

st.write("---")


# ====================================================
# القسم 5: صندوق إضافة وتحديث المعرفة (خاص بالإدارة)
# ====================================================

with st.expander("➕ إضافة معرفة جديدة"):
    new_q = st.text_input("السؤال الجديد:", key="new_q")
    new_a = st.text_area("الإجابة المقترحة له:", key="new_a")
    
    if st.button("حفظ في الذاكرة 💾", key="save_btn"):
        if new_q and new_a:
            try:
                if hasattr(st.session_state.engine, "add_knowledge"):
                    success = st.session_state.engine.add_knowledge(new_q, new_a)
                    if success:
                        st.success("✅ تم حفظ المعلومة بنجاح في قاعدة بياناتك المحلية!")
                        st.balloons()
                    else:
                        st.error("❌ حدث خطأ أثناء الحفظ، يرجى المحاولة مجدداً.")
                else:
                    st.error("❌ خطأ برمجي: دالة إضافة المعرفة (add_knowledge) غير موجودة في ملف inference.py")
            except Exception as e:
                st.error(f"❌ حدث خطأ أثناء محاولة الحفظ: {e}")
        else:
            st.warning("⚠️ يرجى كتابة السؤال والإجابة أولاً قبل الضغط على حفظ.")


# ====================================================
# القسم 6: تذييل الصفحة (Footer)
# ====================================================

st.write("---")
st.markdown("<p style='text-align: center; color: #888;'>🚀 نظام ذكاء اصطناعي محلي يعمل بدون إنترنت</p>", unsafe_allow_html=True)
