import os

# قراءة السجل التعليمي التراكمي دون مسح القديم لضمان البناء المستمر
try:
    with open("saeed_evolution_log.txt", "r", encoding="utf-8") as f:
        evolution_history = f.read()
except FileNotFoundError:
    evolution_history = "No evolution log found yet."

# [Saeed MarketAds] - Saeed LogiC Advanced Evolution & Self-Correction Engine
def apply_arabic_grammar_rules(user_input):
    """
    محرك ذكاء تراكمي شامل: يتعرف على التحيات، الأسئلة الشخصية، استفسارات التسوق،
    ويطبق القواعد النحوية والضمائر والحروف بدقة متناهية تحت راية SaeedMarketAds.
    """
    cleaned_input = user_input.strip().lower()
    
    # 1. الردود الذكية المتنوعة على التحيات والأسئلة العامة
    if any(word in cleaned_input for word in ["صباح الخير", "مساء الخير", "السلام عليكم", "اهلاً", "مرحباً"]):
        return "وعليكم السلام ورحمة الله وبركاته! أهلاً بك. أنا مساعدك الذكي من Saeed MarketAds، كيف يمكنني مساعدتك اليوم؟"
    
    elif any(word in cleaned_input for word in ["من انت", "مين أنت", "من أنت", "ما اسمك"]):
        return "أنا Saeed LogiC، مساعد التسوق الذكي الخاص بك تحت راية Saeed MarketAds، تم برمجتي وتطويري لأكون دليلك الأفضل لعروض الصفقات والكوبونات وتوفير الأموال."
    
    elif any(word in cleaned_input for word in ["كيف حالك", "كيفك", "اخبارك"]):
        return "أنا بأفضل حال وجاهز بكفاءة تامة لخدمتك وبحث أفضل العروض من AliExpress، Noon، و SHEIN!"
    
    elif any(word in cleaned_input for word in ["من برمجك", "من صممك", "صانعك"]):
        return "تم تصميمي وتطويري بواسطة المبرمج الخبير سعيد المسوري (أبو رايد) لأجل إدارة شبكة Saeed MarketAds باحترافية عالية."
    
    elif any(word in cleaned_input for word in ["أين تعمل", "فين تعمل", "مع من تعمل"]):
        return "أنا أعمل هنا في منصة Saeed LogiC الذكية، وأرتبط مباشرة بشبكة تسوق عالمية تشمل نون، شي إن، وآلي إكسبريس."
    
    elif any(word in cleaned_input for word in ["الموضة", "الجديد", "المنتج الجديد"]):
        return "أحدث صيحات الموضة والمنتجات الجديدة متوفرة الآن في عروض المتاجر الكبرى (نون وشي إن). هل تحب أن أبحث لك عن أحدث الكوبونات والخصومات لها؟"
    
    elif any(word in cleaned_input for word in ["الأسعار", "اسعار مناسبة", "خصم"]):
        return "نحن نبحث لك دائماً عن أفضل الأسعار والخصومات المناسبة لميزانيتك عبر شبكة Saeed MarketAds لتوفير أموالك بأقصى دقة."

    # 2. القاموس الموسع للقواعد والضمائر والحروف للتصحيح الذاتي المستمر
    grammar_rules = {
        "هو": "للمذكر المفرد",
        "هي": "للمؤنث المفرد",
        "هما": "للمثنى (مذكر ومؤنث)",
        "هم": "لجمع الذكور أو المختلط",
        "هن": "لجمع الإناث",
        "انا": "للمتكلم المفرد",
        "نحن": "للمتكلمين أو المعظم لنفسه",
        "ان": "حرف توكيد ونصب (تثبيت المعنى)",
        "إنا": "إن + نا للتوكيد الجماعي",
        "و": "حرف عطف للربط والمشاركة"
    }
    
    response_feedback = f"Saeed LogiC Active Memory: Processing input -> '{cleaned_input}'."
    matched = False
    for word, rule in grammar_rules.items():
        if word in cleaned_input:
            response_feedback += f" | Rule Applied [{word}]: {rule}"
            matched = True
            
    if matched:
        return response_feedback

    # 3. رد افتراضي ذكي إذا لم تطابق المدخلات قاعدة أو تحية محددة
    return f"Saeed LogiC Active Memory: تم استلام طلبك '{cleaned_input}' بنجاح. أنا جاهز للبحث عن أفضل الصفقات والعروض المرتبطة بنون، شي إن، أو آلي إكسبريس لأجلك!"

# محاكاة تفاعل ذكي ومستمر
if __name__ == "__main__":
    print("--- Saeed LogiC Pro is Online & Learning ---")
    print(f"Loaded Evolution Memory:\n{evolution_history}")
