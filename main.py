import json
import os

def load_knowledge():
    # تحميل قاعدة المعرفة من الملف الخارجي
    with open('data/knowledge.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def get_logic_response(user_input):
    # تحميل البيانات ديناميكياً
    knowledge = load_knowledge()
    
    # تحويل النص لـ lowercase للبحث
    text = user_input.lower()
    
    # البحث عن نمط (Logic Match) داخل البيانات المستوردة
    for key, response in knowledge.items():
        if key in text:
            return response
            
    return "لا أملك قاعدة بيانات لهذا الاستفسار حالياً، هل تريد إضافته؟"

# اختبار بسيط للتأكد من أن الكود يعمل
if __name__ == "__main__":
    print(get_logic_response("مرحبا"))
