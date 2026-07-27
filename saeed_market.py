import os
import asyncio
import edge_tts

# =====================================================================
# 1. قراءة السجل التعليمي التراكمي
# =====================================================================
try:
    with open("saeed_evolution_log.txt", "r", encoding="utf-8") as f:
        evolution_history = f.read()
except FileNotFoundError:
    evolution_history = "No evolution log found yet."

# =====================================================================
# 2. وظيفة التوليد الصوتي الحقيقي (Neural Voice Synthesis)
# =====================================================================
async def speak_response(text, output_filename="response_audio.mp3"):
    """
    تقوم بتحويل النصوص إلى ملف صوتي ناعم بصوت عربي احترافي باستخدام edge-tts.
    """
    try:
        voice = "ar-SA-ZariyahNeural"  # صوت عربي رسمي
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_filename)
    except Exception as e:
        print(f"Audio generation error: {e}")

def generate_audio_file(text):
    """
    تشغيل وظيفة التوليد الصوتي بشكل متوافق داخل بايثون.
    """
    try:
        asyncio.run(speak_response(text))
    except RuntimeError:
        # حل مشكلة حلقة التنفيذ إذا كانت تعمل مسبقاً في البيئة
        loop = asyncio.get_event_loop()
        loop.run_until_complete(speak_response(text))

# =====================================================================
# 3. محرك الذكاء والردود "بلا حدود" (Saeed LogiC Open-Ended Engine)
# =====================================================================
def apply_arabic_grammar_rules(user_input):
    """
    محرك ذكاء مفتوح بلا حدود: يستقبل أي نص من المستخدم، يحلله، 
    ويقدم رداً تسويقياً ومعلوماتياً متكاملاً، مع توليد الصوت تلقائياً.
    """
    if not user_input:
        user_input = "مرحباً"
        
    cleaned_input = user_input.strip()
    lower_input = cleaned_input.lower()
    reply_text = ""
    
    # قاموس الردود الذكية المباشرة
    if any(w in lower_input for w in ["صباح الخير", "مساء الخير", "السلام عليكم", "اهلاً", "مرحباً"]):
        reply_text = "وعليكم السلام ورحمة الله وبركاته! أهلاً بك يا غالي في منصة Saeed MarketAds. كيف يمكنني مساعدتك اليوم في عالم التسوق والعروض؟"
    
    elif any(w in lower_input for w in ["من انت", "مين أنت", "من أنت", "ما اسمك"]):
        reply_text = "أنا Saeed LogiC، مساعد التسوق الذكي الخاص بك تحت راية Saeed MarketAds، تم برمجتي وتطويري لأكون دليلك الأفضل لعروض الصفقات والكوبونات وتوفير الأموال."
    
    elif any(w in lower_input for w in ["كيف حالك", "كيفك", "اخبارك"]):
        reply_text = "أنا بأفضل حال وجاهز بكفاءة تامة لخدمتك وبحث أفضل العروض من AliExpress، Noon، و SHEIN!"
    
    elif any(w in lower_input for w in ["من برمجك", "من صممك", "صانعك"]):
        reply_text = "تم تصميمي وتطويري بواسطة المبرمج الخبير سعيد المسوري (أبو رايد) لأجل إدارة شبكة Saeed MarketAds باحترافية عالية."
    
    elif any(w in lower_input for w in ["أين تعمل", "فين تعمل", "مع من تعمل"]):
        reply_text = "أنا أعمل هنا في منصة Saeed LogiC الذكية، وأرتبط مباشرة بشبكة تسوق عالمية تشمل نون، شي إن، وآلي إكسبريس."
    
    elif any(w in lower_input for w in ["الموضة", "الجديد", "المنتج الجديد", "موضة"]):
        reply_text = f"أحدث صيحات الموضة والمنتجات الجديدة لطلبك ('{cleaned_input}') متوفرة الآن في عروض المتاجر الكبرى (نون وشي إن). هل تحب أن أبحث لك عن أحدث الكوبونات والخصومات لها؟"
    
    elif any(w in lower_input for w in ["الأسعار", "سعر", "اسعار مناسبة", "خصم", "عروض", "عروضات"]):
        reply_text = f"بخصوص بحثك عن ('{cleaned_input}'): نحن نبحث لك دائماً عن أفضل الأسعار والخصومات المناسبة لميزانيتك عبر شبكة Saeed MarketAds لتوفير أموالك بأقصى دقة."

    else:
        # القواعد النحوية والضمائر
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
        
        matched_rules = []
        for word, rule in grammar_rules.items():
            if word in lower_input:
                matched_rules.append(f"[{word}: {rule}]")
                
        if matched_rules:
            reply_text = f"Saeed LogiC Active Memory: تم تحليل المدخلات '{cleaned_input}' وتطبيق القواعد النحوية التالية: {' | '.join(matched_rules)}."
        else:
            # معالجة مفتوحة "بلا حدود" لأي كلمة أو جملة يكتبها المستخدم
            reply_text = f"يا هلا بطلبك ('{cleaned_input}'). بصفتي مساعدك الذكي تحت راية Saeed MarketAds، أنا جاهز أبحث لك عن أفضل الصفقات، المنتجات، والكوبونات وتوفير أموالك. هل تحب أربط لك هذا الطلب مع عروض نون، شي إن، أو آلي إكسبريس؟"

    # توليد ملف الصوت تلقائياً لكل رد
    generate_audio_file(reply_text)
    
    return reply_text

# =====================================================================
# 4. تشغيل النظام واختباره
# =====================================================================
if __name__ == "__main__":
    print("--- Saeed LogiC Pro (Open-Ended & Audio Engine) is Online ---")
    print(f"Loaded Evolution Memory:\n{evolution_history}")
