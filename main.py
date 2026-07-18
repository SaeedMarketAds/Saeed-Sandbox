import streamlit as st
import json
import os

# 1. إعداد الصفحة والاسم المعتمد الفخم
st.set_page_config(page_title="Saeed Logic", page_icon="🛍", layout="centered")

# 2. إدارة البيانات محلياً في نفس الملف (تجنباً لأي خطأ استيراد)
DATA_DIR = "data"
FILE_PATH = os.path.join(DATA_DIR, "shopping_data.json")
os.makedirs(DATA_DIR, exist_ok=True)

def load_shopping_data():
    """قراءة قاعدة بيانات التسوق المحلية بأمان"""
    default_data = {
        "مرحبا": "أهلاً بك في مساعد التسوق الخاص بك! 🛍 كيف يمكنني مساعدتك في العروض والروابط اليوم؟",
        "شي إن": "عروض شي إن (SHEIN) الحصرية جاهزة ومخصصة! يمكنك تعديل الروابط والكوبونات هنا دائماً.",
        "علي إكسبريس": "أهلاً بك! هنا تجد وتدير روابط عروض علي إكسبريس القوية التابعة لك.",
        "نون": "كوبونات وعروض متجر نون المحدثة محفوظة في ذاكرتك المحلية."
    }
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=4)
        return default_data
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return default_data

def save_shopping_data(data):
    """حفظ العروض والروابط الجديدة فوراً"""
    try:
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception:
        return False

# تحميل الذاكرة المحلية للتسوق
shopping_memory = load_shopping_data()

# 3. تصميم واجهة التطبيق المتطابقة مع هويتك الجديدة (مساعد التسوق)
st.markdown("<h1 style='text-align: right;'> S_L </h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: right;'>😀 Saeed Logic</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: right; color: #ff4b4b;'>مساعد التسوق 🛍</h3>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: right; color: #888;'>نظامك المحلي المستقر لإدارة وتتبع العروض، الكوبونات، والروابط 100% بدون إنترنت</h5>", unsafe_allow_html=True)
st.write("---")

# حقل البحث والاسترجاع السريع
user_input = st.text_input("ابحث عن متجر، كود، أو عرض محدد:", placeholder="اكتب اسم المتجر أو الكلمة المفتاحية هنا...", key="shop_search")

if user_input:
    q_clean = user_input.strip().lower()
    found = False
    
    # البحث المرن في الذاكرة المحلية
    for key, val in shopping_memory.items():
        if key.lower() in q_clean or q_clean in key.lower():
            st.success(f"🔍 **النتيجة المخزنة:**\n\n{val}")
            found = True
            break
            
    if not found:
        st.info("💡 هذا العرض أو الكلمة غير مسجلة في ذاكرة التسوق حالياً. يمكنك إضافتها بالأسفل لكي أحفظها لك فوراً!")

st.write("---")

# 4. قسم إضافة وتحديث عروض التسوق
with st.expander("➕ إضافة كود خصم أو رابط تسوق جديد"):
    new_key = st.text_input("الكلمة المفتاحية (مثال: كود نون الجديد أو فستان شي إن):", key="new_key")
    new_val = st.text_area("تفاصيل العرض، الكوبون، أو رابط الآفلييت المباشر:", key="new_val")
    
    if st.button("حفظ في ذاكرة المساعد 💾", key="save_shop_btn"):
        if new_key and new_val:
            shopping_memory[new_key.strip()] = new_val.strip()
            if save_shopping_data(shopping_memory):
                st.success("✅ تم حفظ العرض بنجاح في قاعدة بياناتك المحلية لـ Saeed Logic!")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ حدث خطأ غير متوقع أثناء الحفظ.")
        else:
            st.warning("⚠️ يرجى كتابة الكلمة المفتاحية والتفاصيل أولاً قبل الحفظ.")

st.write("---")
st.markdown("<p style='text-align: center; color: #888;'>🚀 مساعد التسوق الخاص بك يعمل الآن بثبات وأمان كاملين</p>", unsafe_allow_html=True)
