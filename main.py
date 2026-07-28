import os
import json
import asyncio
import edge_tts
from colorama import init, Fore, Style
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from datetime import datetime

# تهيئة الألوان (Windows/Linux)
init(autoreset=True)
console = Console()

# ============================
# 1. تحميل الذاكرة والتاريخ
# ============================
MEMORY_FILE = "conversation.json"
ERROR_LOG_FILE = "error_corrections.json"

def load_memory():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"history": []}

def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_corrections():
    try:
        with open(ERROR_LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_corrections(corr):
    with open(ERROR_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(corr, f, ensure_ascii=False, indent=2)

memory = load_memory()
corrections = load_corrections()

# ============================
# 2. توليد الصوت
# ============================
async def speak_response(text, filename="response.mp3"):
    try:
        voice = "ar-SA-ZariyahNeural"
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(filename)
        console.print(f"[green]✔️ تم توليد الصوت في {filename}[/green]")
    except Exception as e:
        console.print(f"[red]❌ خطأ في الصوت: {e}[/red]")

def generate_audio(text):
    try:
        asyncio.run(speak_response(text))
    except RuntimeError:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.create_task(speak_response(text))
        else:
            loop.run_until_complete(speak_response(text))

# ============================
# 3. محرك الذكاء (Gemini + Knowledge)
# ============================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")

if GEMINI_API_KEY != "YOUR_API_KEY_HERE":
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None
    console.print("[yellow]⚠️ لم يتم تعيين مفتاح Gemini، سيُستخدم المحرك الاحتياطي.[/yellow]")

def load_knowledge():
    """تحميل قاعدة المعرفة من knowledge.json"""
    try:
        with open("knowledge.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"merchants": {}}

def generate_intelligent_response(user_input):
    """توليد رد ذكي باستخدام Gemini مع دمج قاعدة المعرفة والتصحيحات"""
    # 1. تحميل قاعدة المعرفة
    knowledge = load_knowledge()
    
    # 2. استخراج الكوبونات
    coupons_text = ""
    for merchant, data in knowledge.get("merchants", {}).items():
        if data.get("coupons"):
            coupons_text += f"\n🎫 كوبونات {merchant}: {', '.join(data['coupons'])}"
    
    # 3. بناء السياق من آخر 5 محادثات
    context = "\n".join([f"س: {h['user']}\nج: {h['bot']}" for h in memory["history"][-5:]])
    
    # 4. إضافة التصحيحات السابقة
    corrections_text = ""
    for wrong, correct in corrections.items():
        corrections_text += f"تصحيح: عندما قلت '{wrong}' كان الأفضل أن أقول '{correct}'.\n"
    
    # 5. بناء الـ Prompt الكامل
    prompt = f"""
أنت Saeed LogiC، مساعد تسوق ذكي تحت ماركة Saeed MarketAds.
مهمتك: مساعدة المستخدم في العثور على أفضل العروض والكوبونات من نون، شي إن، علي إكسبريس.
أنت تتحدث بالعامية الخليجية الفصحى، ودود، ومفيد.

سياق المحادثة الأخيرة:
{context}

تصحيحات سابقة يجب مراعاتها:
{corrections_text}

المعلومات الإضافية عن العروض والكوبونات المتوفرة حالياً:
{coupons_text}

المستخدم يقول الآن: "{user_input}"

قدِّم رداً شاملاً، مع ذكر العروض إن أمكن، وإذا كان السؤال خارج التسوق، استجب بلطف واقترح كيف يمكنك مساعدته في التسوق أيضاً.
"""
    try:
        if model:
            response = model.generate_content(prompt)
            reply = response.text.strip()
        else:
            reply = fallback_reply(user_input)
    except Exception as e:
        console.print(f"[red]خطأ في Gemini: {e}[/red]")
        reply = fallback_reply(user_input)
    
    return reply

def fallback_reply(user_input):
    """محرك احتياطي يعتمد على الكلمات المفتاحية"""
    lower = user_input.lower()
    if any(w in lower for w in ["صباح", "مساء", "السلام", "اهلاً", "مرحباً"]):
        return "وعليكم السلام ورحمة الله وبركاته! أهلاً بك يا غالي في منصة Saeed MarketAds. كيف يمكنني مساعدتك اليوم في عالم التسوق والعروض؟"
    elif any(w in lower for w in ["من انت", "مين أنت"]):
        return "أنا Saeed LogiC، مساعد التسوق الذكي الخاص بك تحت راية Saeed MarketAds، تم برمجتي لأكون دليلك الأفضل لعروض الصفقات والكوبونات."
    elif any(w in lower for w in ["كيف حالك"]):
        return "أنا بأفضل حال وجاهز بكفاءة تامة لخدمتك وبحث أفضل العروض من AliExpress، Noon، و SHEIN!"
    else:
        return f"يا هلا بطلبك ('{user_input}'). بصفتي مساعدك الذكي، أنا جاهز أبحث لك عن أفضل الصفقات والكوبونات وتوفير أموالك. هل تحب أربط لك هذا الطلب مع عروض نون، شي إن، أو آلي إكسبريس؟"

# ============================
# 4. آلية التصحيح والتعلم
# ============================
def correct_response(user_input, bot_response, user_feedback):
    if "خطأ:" in user_feedback or "تصحيح:" in user_feedback:
        correction = user_feedback.split(":", 1)[1].strip()
        corrections[user_input] = correction
        save_corrections(corrections)
        console.print("[green]✔️ تم حفظ التصحيح، سأتعلم منه في المرات القادمة![/green]")
        return correction
    return None

# ============================
# 5. حلقة المحادثة الرئيسية
# ============================
def main_loop():
    console.print(Panel.fit("[bold cyan]🤖 Saeed LogiC Pro - مساعد التسوق الذكي (بلا حدود)[/bold cyan]",
                            border_style="cyan"))
    console.print("[yellow]📢 اكتب 'خروج' لإنهاء الجلسة، أو 'تصحيح: ...' لإصلاح رد سابق.[/yellow]")
    console.print("[magenta]💡 يمكنك سؤالي عن أي شيء، وسأبحث لك عن أفضل العروض![/magenta]\n")

    while True:
        user_input = input(Fore.GREEN + "👤 أنت: " + Style.RESET_ALL)
        if user_input.lower() in ["خروج", "quit", "exit"]:
            console.print("[red]مع السلامة، نتمنى لك يوماً سعيداً![/red]")
            break

        bot_reply = generate_intelligent_response(user_input)
        console.print(Panel(Markdown(bot_reply), title="[bold blue]🤖 Saeed LogiC[/bold blue]", border_style="blue"))
        generate_audio(bot_reply)

        memory["history"].append({"user": user_input, "bot": bot_reply, "time": str(datetime.now())})
        save_memory(memory)

        feedback = input(Fore.YELLOW + "📝 هل هذا الرد صحيح؟ (اضغط Enter للموافقة، أو اكتب 'تصحيح: ...' لتعديله): " + Style.RESET_ALL)
        if feedback.strip():
            correction = correct_response(user_input, bot_reply, feedback)
            if correction:
                console.print(f"[cyan]تم التحديث، سأستخدم التصحيح: {correction}[/cyan]")
                generate_audio(correction)

if __name__ == "__main__":
    main_loop()
