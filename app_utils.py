# ===================================================================
# app_utils.py - الملف الموحّد (المخ) لكل دوال Saeed LogiC Pro
# ===================================================================

import os
import json
import asyncio
import edge_tts
from datetime import datetime

# ===================================================================
# 1. دوال تحميل وحفظ الملفات (الذاكرة، التصحيحات، المعرفة)
# ===================================================================

MEMORY_FILE = "conversation.json"
ERROR_LOG_FILE = "error_corrections.json"
KNOWLEDGE_FILE = "knowledge.json"

def load_json(file, default):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# تحميل البيانات العامة (تُستخدم في كل الملفات)
memory = load_json(MEMORY_FILE, {"history": []})
corrections = load_json(ERROR_LOG_FILE, {})
knowledge = load_json(KNOWLEDGE_FILE, {"merchants": {}})

# ===================================================================
# 2. دوال توليد الصوت (edge-tts)
# ===================================================================

async def speak_async(text, filename="temp_audio.mp3"):
    try:
        communicate = edge_tts.Communicate(text, "ar-SA-ZariyahNeural")
        await communicate.save(filename)
        return filename
    except:
        return None

def generate_audio(text):
    """توليد ملف صوتي من النص وإرجاع مساره"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(speak_async(text))
        loop.close()
        return result
    except:
        return None

# ===================================================================
# 3. محرك الذكاء (Gemini + Knowledge + Corrections)
# ===================================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
use_gemini = False
model = None

if GEMINI_API_KEY != "YOUR_API_KEY_HERE":
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        use_gemini = True
    except:
        pass

def fallback_reply(user_input):
    """المحرك الاحتياطي (عند عدم توفر Gemini)"""
    lower = user_input.lower()
    if any(w in lower for w in ["صباح", "مساء", "السلام", "اهلاً"]):
        return "وعليكم السلام ورحمة الله! أهلاً بك في Saeed LogiC Pro 🌟"
    elif "كيف حالك" in lower:
        return "أنا بخير وسعادة، وجاهز لأبحث لك عن أرخص العروض! 😍"
    elif "عرض" in lower or "كوبون" in lower or "خصم" in lower:
        coupons = ""
        for m, d in knowledge.get("merchants", {}).items():
            if d.get("coupons"):
                coupons += f"🎫 {m}: {', '.join(d['coupons'])}\n"
        return f"تفضل أقوى العروض:\n{coupons}\nهل تبحث عن متجر معين؟"
    else:
        return f"يا هلا بطلبك ('{user_input}'). أنا جاهز أبحث عن أفضل الصفقات. هل تحب تربط هذا الطلب مع نون، شي إن، أو علي إكسبريس؟"

def get_ai_reply(user_input):
    """توليد رد ذكي باستخدام Gemini (مع السياق والكوبونات والتصحيحات)"""
    # تحضير الكوبونات
    coupons_text = ""
    for merchant, data in knowledge.get("merchants", {}).items():
        if data.get("coupons"):
            coupons_text += f"\n🎫 {merchant}: {', '.join(data['coupons'])}"

    # السياق من آخر 5 محادثات
    context = "\n".join([
        f"س: {h['user']}\nج: {h['bot']}" 
        for h in memory["history"][-5:]
    ])

    # التصحيحات السابقة
    corrections_text = ""
    for wrong, correct in corrections.items():
        corrections_text += f"تصحيح: '{wrong}' -> '{correct}'\n"

    # بناء الـ Prompt
    prompt = f"""
أنت Saeed LogiC، مساعد تسوق ذكي تحت ماركة Saeed MarketAds.
مهمتك: مساعدة المستخدم في العثور على أفضل العروض والكوبونات من نون، شي إن، علي إكسبريس.
أنت تتحدث بالعامية الخليجية الفصحى، ودود، ومفيد.

سياق المحادثة الأخيرة:
{context}

تصحيحات سابقة يجب مراعاتها:
{corrections_text}

الكوبونات والعروض المتوفرة حالياً:
{coupons_text}

المستخدم يقول الآن: "{user_input}"

قدِّم رداً شاملاً وجذاباً، مع ذكر العروض إن أمكن.
"""

    try:
        if use_gemini and model:
            response = model.generate_content(prompt)
            reply = response.text.strip()
        else:
            reply = fallback_reply(user_input)
    except:
        reply = fallback_reply(user_input)

    return reply

# ===================================================================
# 4. دوال التصحيح والتعلم
# ===================================================================

def correct_response(user_input, user_feedback):
    """معالجة طلب التصحيح من المستخدم وحفظه"""
    if "خطأ:" in user_feedback or "تصحيح:" in user_feedback:
        correction = user_feedback.split(":", 1)[1].strip()
        corrections[user_input] = correction
        save_json(ERROR_LOG_FILE, corrections)
        return correction
    return None

def save_conversation(user_input, bot_reply):
    """حفظ المحادثة في ملف الذاكرة"""
    memory["history"].append({
        "user": user_input,
        "bot": bot_reply,
        "time": str(datetime.now())
    })
    save_json(MEMORY_FILE, memory)
