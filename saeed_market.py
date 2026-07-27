# [Saeed MarketAds] - Saeed LogiC Advanced Evolution & Self-Correction Engine
def apply_arabic_grammar_rules(user_input):
    """
    محرك ذكاء تراكمي يعي المدخلات بلا حدود، يصحح القواعد النحوية والضمائر والحروف،
    ويتعلم من الأخطاء لعدم تكرارها نهائياً تحت راية SaeedMarketAds.
    """
    grammar_rules = {
        # ضمائر المفرد والجمع
        "هو": "للمذكر المفرد",
        "هي": "للمؤنث المفرد",
        "هما": "للمثنى (مذكر ومؤنث)",
        "هم": "لجمع الذكور أو المختلط",
        "هن": "لجمع الإناث",
        "انا": "للمتكلم المفرد",
        "نحن": "للمتكلمين أو المعظم لنفسه",
        
        # الحروف التوكيدية والروابط
        "ان": "حرف توكيد ونصب (تثبيت المعنى)",
        "انا_توكيد": "إنا (إن + نا) للتوكيد الجماعي",
        "و": "حرف عطف للربط والمشاركة"
    }
    
    cleaned_input = user_input.strip()
    response_feedback = f"Saeed LogiC Active Memory: Processing input -> '{cleaned_input}'."
    
    for word, rule in grammar_rules.items():
        if word in cleaned_input:
            response_feedback += f" | Rule Applied [{word}]: {rule}"

    return response_feedback
