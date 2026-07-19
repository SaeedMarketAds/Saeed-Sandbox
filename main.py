import streamlit as st
import google.generativeai as genai
from engine.inference import search_knowledge_base

# إعدادات الصفحة الافتراضية
st.set_page_config(page_title="Saeed LogiC Pro", page_icon="🚀", layout="centered")

# إعداد مفتاح الـ API الخاص بـ Gemini (استبدله بمفتاحك الحقيقي)
# يمكنك الحصول عليه مجاناً من Google AI Studio
# ربط المفتاح بشكل آمن ومشفر من إعدادات السيرفر
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])


st.title("Saeed LogiC Pro 🚀")
st.subheader("نظام محلي لدمج العروض والكوبونات")

# قاموس التحيات السريعة لتوفير استهلاك الـ API
GREETINGS_MAP = {
    ("السلام عليكم", "سلام"): "وعليكم السلام ورحمة الله وبركاته! أهلاً بك في مساعد التسوق الخاص بك. كيف يمكنني مساعدتك في العروض والكوبونات اليوم؟",
    ("صباح الخير", "صباح النور"): "صباح النور والسرور! كيف يمكنني مساعدتك في العروض اليوم؟",
    ("مساء الخير", "مساء النور"): "مساء النور والسرور! كيف يمكنني مساعدتك في العروض اليوم؟",
    ("مرحبا", "أهلا", "هلا"): "أهلاً وسهلاً بك! تفضل بسؤالك عن الكوبونات المتاحة."
}

user_input = st.chat_input("...اسألني عن العروض المتاحة")

if user_input:
    # 1. إظهار رسالة المستخدم
    with st.chat_message("user"):
        st.write(user_input)
        
    reply = None

    # 2. الخطوة الأولى: فحص التحيات السريعة
    for keywords, response_text in GREETINGS_MAP.items():
        if any(kw in user_input.strip() for kw in keywords):
            reply = response_text
            break

    # 3. الخطوة الثانية: إذا لم تكن تحية، ابحث في قاعدة البيانات المحلية JSON
    if reply is None:
        local_result = search_knowledge_base(user_input)
        
        # تأكد أن دالة البحث في كودك تعود بنص واضح في حال عدم وجود الكوبون
        # سنفترض أنها تعود بـ None أو نص يفيد بعدم العثور على الكوبون
        if local_result and "لم أجد" not in local_result:
            reply = local_result

    # 4. الخطوة الثالثة: إذا لم يجد النظام تحية ولا كوبون محلي، يستعين بذكاء Gemini
    if reply is None:
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            # توجيه أمر صارم للذكاء الاصطناعي ليتحدث باسم تطبيقك فقط
            prompt = (
                f"أنت مساعد تسوق ذكي مدمج في تطبيق (Saeed LogiC Pro). "
                f"أجب باختصار شديد، وبلباقة، وبلهجة ترحيبية وتذكر دائماً أنك مساعد تسوق. "
                f"السؤال: {user_input}"
            )
            response = model.generate_content(prompt)
            reply = response.text
        except Exception as e:
            reply = "أهلاً بك! لم أجد كوبوناً متاحاً لهذا الطلب حالياً، يرجى المحاولة لاحقاً."

    # 5. عرض الرد النهائي للمستخدم
    with st.chat_message("assistant"):
        st.write(reply)
