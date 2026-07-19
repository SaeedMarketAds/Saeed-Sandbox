import os
import json
import streamlit as st
from datetime import datetime

# === 1. حل مشكلة تعارض الملفات والمجلدات وتجهيز البيئة ===
for folder in ["data", "engine"]:
    if os.path.exists(folder) and os.path.isfile(folder):
        os.remove(folder)  # حذف الملف إذا وجد ليفسح المجال للمجلد
    os.makedirs(folder, exist_ok=True)

# === 2. تهيئة ملفات البيانات الافتراضية ===
def init_data_files():
    knowledge_path = "data/knowledge.json"
    conversation_path = "data/conversation.json"
    
    if not os.path.exists(knowledge_path):
        with open(knowledge_path, "w", encoding="utf-8") as f:
            json.dump({"coupons": [], "offers": []}, f, ensure_ascii=False, indent=2)
    
    if not os.path.exists(conversation_path):
        with open(conversation_path, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

init_data_files()

# === 3. استيراد المحرك ===
try:
    from engine.inference import InferenceEngine
except ImportError:
    st.error("❌ خطأ: لم يتم العثور على ملف المحرك في مسار engine/inference.py")
    st.stop()

# === 4. تهيئة المحرك في جلسة Streamlit ===
if "engine" not in st.session_state:
    try:
        st.session_state.engine = InferenceEngine()
    except Exception as e:
        st.error(f"❌ فشل تهيئة المحرك: {str(e)}")
        st.stop()

# === 5. واجهة المستخدم والتصميم ===
st.set_page_config(
    page_title="🛍️ Saeed LogiC",
    page_icon="🛒",
    layout="wide"
)

st.title("🛍️ مساعد التسوق Saeed LogiC")
st.caption("نظامك المحلي المستقر لتتبع العروض والكوبونات - 100% بدون إنترنت")

# === 6. الشريط الجانبي والقائمة ===
with st.sidebar:
    st.header("📋 القائمة")
    menu = st.radio(
        "اختر الإجراء",
        ["🔍 البحث عن عرض", "➕ إضافة كود خصم", "📊 عرض الكوبونات", "💬 المحادثات"]
    )
    st.divider()
    st.caption(f"🟢 النظام يعمل بثبات | {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# === 7. معالجة الصفحات والعمليات ===
if menu == "🔍 البحث عن عرض":
    st.subheader("🔍 ابحث عن متجر، كود، أو عرض محدد")
    search_term = st.text_input("🔎 كلمة البحث", placeholder="مثال: كود نون الجديد أو فستان شي إن")
    
    if st.button("🔍 بحث", use_container_width=True):
        if search_term:
            result = st.session_state.engine.search(search_term)
            if result:
                st.success("✅ النتائج المطابقة:")
                st.json(result)
            else:
                st.info("ℹ️ لا توجد نتائج مطابقة لكلمة البحث هذه.")
        else:
            st.warning("⚠️ الرجاء إدخال كلمة بحث")

elif menu == "➕ إضافة كود خصم":
    st.subheader("➕ إضافة كود خصم أو عرض جديد")
    
    with st.form("add_coupon_form"):
        store = st.text_input("🏪 اسم المتجر", placeholder="مثال: نون، شي إن، أمازون")
        code = st.text_input("🔑 كود الخصم", placeholder="مثال: SAVE20")
        description = st.text_area("📝 تفاصيل العرض", placeholder="وصف العرض أو الكوبون")
        link = st.text_input("🔗 رابط العرض (اختياري)", placeholder="https://example.com")
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("💾 حفظ", use_container_width=True)
        with col2:
            reset = st.form_submit_button("🔄 إعادة تعيين", use_container_width=True)
        
        if submitted:
            if store and code and description:
                success = st.session_state.engine.add_coupon(store, code, description, link)
                if success:
                    st.success("✅ تم حفظ الكوبون بنجاح!")
                    st.balloons()
                else:
                    st.error("❌ فشل حفظ الكوبون")
            else:
                st.warning("⚠️ الرجاء ملء جميع الحقول المطلوبة")

elif menu == "📊 عرض الكوبونات":
    st.subheader("📊 جميع الكوبونات والعروض")
    coupons = st.session_state.engine.get_all_coupons()
    
    if coupons:
        for i, coupon in enumerate(coupons):
            with st.expander(f"🏪 {coupon.get('store', 'غير معروف')} - {coupon.get('code', '')}"):
                st.write(f"**📝 التفاصيل:** {coupon.get('description', 'لا يوجد')}")
                if coupon.get('link'):
                    st.write(f"**🔗 الرابط:** [{coupon['link']}]({coupon['link']})")
                st.caption(f"📅 تاريخ الإضافة: {coupon.get('date', 'غير معروف')}")
                
                if st.button(f"🗑️ حذف", key=f"del_{i}"):
                    if st.session_state.engine.delete_coupon(i):
                        st.rerun()
    else:
        st.info("📭 لا توجد كوبونات محفوظة حالياً.")

elif menu == "💬 المحادثات":
    st.subheader("💬 سجل المحادثات والنشاط")
    conversations = st.session_state.engine.get_conversations()
    
    if conversations:
        for conv in conversations[-10:]:  # عرض آخر 10 سجلات
            with st.chat_message(conv.get("role", "user")):
                st.write(conv.get("content", ""))
    else:
        st.info("📭 لا توجد محادثات مسجلة بعد.")
