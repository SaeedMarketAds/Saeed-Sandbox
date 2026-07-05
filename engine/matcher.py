# منطق استنتاجي بسيط
knowledge_base = {
    "سعر": "سعر المنتج يعتمد على العرض والطلب.",
    "مرحبا": "أهلاً بك، أنا SaeeD LogiC، كيف يمكنني مساعدتك منطقياً اليوم؟",
    "وداعاً": "إلى اللقاء، سأكون هنا في الذاكرة بانتظارك."
}

def get_logic_response(user_input):
    # تحويل النص لـ lowercase للبحث
    text = user_input.lower()
    
    # البحث عن نمط (Logic Match)
    for key in knowledge_base:
        if key in text:
            return knowledge_base[key]
    
    return "لا أملك قاعدة بيانات لهذا الاستفسار حالياً، هل تريد إضافته؟"

