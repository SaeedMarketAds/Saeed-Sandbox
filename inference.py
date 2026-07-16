import difflib
import re
from utils import load_json, save_json, clean_text

KNOWLEDGE_PATH = "data/knowledge.json"
MEMORY_PATH = "/tmp/conversation.json"

# حد التشابه المقبول (0 إلى 1). كل ما زاد، صارت المطابقة أدق وأصعب.
SIMILARITY_THRESHOLD = 0.55


def normalize_arabic(text: str) -> str:
    """توحيد الحروف العربية المتشابهة لتحسين المطابقة."""
    text = clean_text(text)
    replacements = {
        "أ": "ا", "إ": "ا", "آ": "ا",
        "ة": "ه",
        "ى": "ي",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip().lower()


class InferenceEngine:
    """
    محرك استدلال محلي بالكامل - بدون أي اتصال إنترنت أو مفتاح API.
    يعتمد على:
    1) التطابق الحرفي المباشر (الأسرع)
    2) التشابه التقريبي بين الجمل (يفهم الأخطاء الإملائية والصياغات القريبة)
    3) التشابه بالكلمات المفتاحية المشتركة
    """

    def __init__(self):
        self.knowledge = load_json(KNOWLEDGE_PATH)MEMORY_PATH = "/tmp/conversation.json"
        self.memory = load_json(MEMORY_PATH)
        self._normalized_keys = {
            normalize_arabic(k): k for k in self.knowledge.keys()
        }

    def _exact_match(self, question: str) -> str | None:
        return self.knowledge.get(question)

    def _fuzzy_match(self, question: str) -> str | None:
        norm_q = normalize_arabic(question)
        candidates = list(self._normalized_keys.keys())
        matches = difflib.get_close_matches(
            norm_q, candidates, n=1, cutoff=SIMILARITY_THRESHOLD
        )
        if matches:
            original_key = self._normalized_keys[matches[0]]
            return self.knowledge[original_key]
        return None

    def _keyword_match(self, question: str) -> str | None:
        q_words = set(normalize_arabic(question).split())
        if not q_words:
            return None

        best_score = 0
        best_answer = None
        for norm_key, original_key in self._normalized_keys.items():
            key_words = set(norm_key.split())
            if not key_words:
                continue
            overlap = len(q_words & key_words) / len(q_words | key_words)
            if overlap > best_score:
                best_score = overlap
                best_answer = self.knowledge[original_key]

        if best_score >= 0.34:
            return best_answer
        return None

    def answer(self, question: str) -> str:
        q = clean_text(question)

        result = (
            self._exact_match(q)
            or self._fuzzy_match(q)
            or self._keyword_match(q)
        )

        if result is None:
            result = "عذرًا، لم أجد إجابة مناسبة في قاعدة المعرفة حتى الآن. ساعدني بتوسيعها!"

        self.memory[q] = result
        save_json(MEMORY_PATH, self.memory)
        return result
