hereimport os
from colorama import init, Fore, Style
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from app_utils import (
    get_ai_reply, generate_audio, memory, corrections, 
    save_conversation, correct_response
)

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

        bot_reply = get_ai_reply(user_input)
        console.print(Panel(Markdown(bot_reply), title="[bold blue]🤖 Saeed LogiC[/bold blue]", border_style="blue"))
        generate_audio(bot_reply)
        save_conversation(user_input, bot_reply)

        feedback = input(Fore.YELLOW + "📝 هل هذا الرد صحيح؟ (اضغط Enter للموافقة، أو اكتب 'تصحيح: ...' لتعديله): " + Style.RESET_ALL)
        if feedback.strip():
            correction = correct_response(user_input, feedback)
            if correction:
                console.print(f"[cyan]تم التحديث، سأستخدم التصحيح: {correction}[/cyan]")
                generate_audio(correction)

if __name__ == "__main__":
    main_loop()
