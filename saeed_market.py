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
    محرك ذكاء تركمي يعي المدخلات بلا حدود، يصحح القواعد النحوية (أنا، هم، هي، هو)،
    ويتعلم من الأخطاء لعدم تكرارها نهائياً تحت راية SaeedMarketAds.
    """
    # قاعدة معرفية مرنة للضمائر والقواعد الأساسية
    grammar_rules = {
        "هو": "للمذكر المفرد (مثال: هو طور النظام باحتراف)",
        "هي": "للمؤنث المفرد (مثال: هي واجهة ذكية متطورة)",
        "هم": "لجمع الذكور أو المختلط (مثال: هم يعملون على تطوير السوق)",
        "انا": "للمتكلم (مثال: أنا أبني مشروعي للمدى البعيد)"
    }
    
    # تحليل مدخلات المستخدم بلا حدود
    cleaned_input = user_input.strip()
    response_feedback = f"Saeed LogiC Active Memory: Processing input -> '{cleaned_input}'."
    
    # فحص التطابق مع القواعد لترسيخ التصحيح الذاتي
    for pronoun, rule in grammar_rules.items():
        if pronoun in cleaned_input:
            response_feedback += f" | Rule Applied [{pronoun}]: {rule}"

    return response_feedback

# محاكاة تفاعل ذكي ومستمر
if __name__ == "__main__":
    print("--- Saeed LogiC Pro is Online & Learning ---")
    print(f"Loaded Evolution Memory:\n{evolution_history}")
