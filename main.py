import sys
from inference import InferenceEngine

def main():
    print("="*50)
    print("  Saeed Logic - نظام التحقق المحلي  ")
    print("="*50)
    
    # طلب كلمة المرور (مؤقتاً للتجربة اجعلها 1234)
    password = input("Enter Admin Password: ")
    
    if password != "1234":
        print("\n[X] كلمة المرور غير صحيحة. تم رفض الوصول.")
        sys.exit(0)

    print("\n[✓] تم التحقق بنجاح! جاري تشغيل المحرك...\n")
    engine = InferenceEngine()

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['خروج', 'exit']:
                print("تم إغلاق النظام.")
                break
                
            if not user_input.strip():
                continue

            bot_response = engine.get_response(user_input)
            print(f"Saeed Logic: {bot_response}\n")

        except KeyboardInterrupt:
            print("\nتم إنهاء الجلسة.")
            sys.exit(0)

if __name__ == "__main__":
    main()
