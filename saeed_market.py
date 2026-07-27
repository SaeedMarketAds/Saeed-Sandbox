# قراءة السجل التعليمي التراكمي دون مسح القديم
try:
    with open("saeed_evolution_log.txt", "r", encoding="utf-8") as f:
        evolution_history = f.read()
except FileNotFoundError:
    evolution_history = "No evolution log found yet."
