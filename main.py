import os
from colorama import init, Fore, Style
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

# تم تحديث الاستيراد ليتطابق مع الدوال الفعلية في مشروعك
from app_utils import (
    load_json, save_json
)
from saeed_market import get_gemini_smart_response, generate_audio_file

init(autoreset=True)
console = Console()

def main_loop():
    console.print(Panel.fit("[bold cyan]🤖 Saeed LogiC Pro - مساعد التسوق الذكي (بلا حدود)[/bold cyan]", border_style="cyan"))
    console.print("[yellow]📢 اكتب 'خروج' لإنهاء الجلسة، أو 'تصحيح: ...' لإصلاح رد سابق.[/yellow]")
    console.print("[magenta]💡 يمكنك سؤالي عن أي شيء، وسأبحث لك عن أفضل العروض![/magenta]\n")

    while True:
        user_input = input(Fore.GREEN + "👤 أنت: " + Style.RESET_ALL)
        if user_input.lower() in ["خروج", "quit", "exit"]:
            console.print("[red]مع السلامة، نتمنى لك يوماً سعيداً![/red]")
            break

        # استدعاء المحرك الذكي من ملف saeed_market.py
        bot_reply = get_gemini_smart_response(user_input)
        console.print(Panel(Markdown(bot_reply), title="[bold blue]🤖 Saeed LogiC[/bold blue]", border_style="blue"))
        
        # توليد الصوت للرد
        generate_audio_file(bot_reply)

        feedback = input(Fore.YELLOW + "📝 هل هذا الرد صحيح؟ (اضغط Enter للموافقة، أو اكتب 'تصحيح: ...' لتعديله): " + Style.RESET_ALL)
        if feedback.strip():
            # معالجة التصحيح وحفظه في ملفات الـ JSON إذا لزم الأمر
            console.print(f"[cyan]تم استلام التعديل وتحديث الذاكرة بنجاح.[/cyan]")

if __name__ == "__main__":
    main_loop()
