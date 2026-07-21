import google.generativeai as genai

# تهيئة المفتاح
genai.configure(api_key="YOUR_API_KEY")

print("--- النماذج المتاحة للحساب ---")
for model in genai.list_models():
    print(model.name)

