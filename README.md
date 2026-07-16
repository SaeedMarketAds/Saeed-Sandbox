# 🧠 SaeeD LogiC

ذكاء اصطناعي هجين — قاعدة معرفة سريعة + Gemini (مجاني) للأسئلة المفتوحة.

## الهيكل
```
Saeed-Logic/
│
├── data/
│   └── knowledge.json        # قاعدة المعرفة
│
├── engine/
│   ├── inference.py          # محرك الاستدلال
│   └── utils.py              # دوال مساعدة
│
├── memory/
│   └── conversation.json     # سجل المحادثات
│
├── main.py                   # تشغيل Streamlit
├── requirements.txt
└── README.md
```

## طريقة الإعداد
1. اسحب مفتاح Gemini مجاني من https://aistudio.google.com
2. في Streamlit Cloud → Settings → Secrets، ضيف:
   ```
   GEMINI_API_KEY = "مفتاحك هنا"
   ```
3. لا تكتب المفتاح أبدًا داخل الكود مباشرة — خليه دايمًا في Secrets.

## كيف يشتغل
1. أي سؤال يدور أول في `data/knowledge.json` (مطابقة مباشرة، سريعة، مجانية دايمًا).
2. لو ما فيه تطابق، يروح لـ `gemini-3.5-flash` (مجاني ضمن الحد اليومي).
3. كل سؤال وجواب يُحفظ في `memory/conversation.json`.

## ملاحظة عن الموديل
اعتبارًا من 2026، جوجل أوقفت `gemini-1.5-flash`. الموديلات المجانية الحالية هي
`gemini-3.5-flash` و `gemini-3.1-flash-lite`. المشروع يستخدم `gemini-3.5-flash` افتراضيًا.
