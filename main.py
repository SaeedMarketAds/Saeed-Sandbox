import sys
import hashlib
from inference import InferenceEngine

# كلمة المرور الافتراضية مشفرة بـ SHA-256 (مثال لكلمة مرور: "saeed2026")
# يمكنك تغيير الهاش لاحقاً لحماية نظامك
ADMIN_PASSWORD_HASH = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"

def verify_admin():
    print("="*50)
    print("  مرحباً بك في Saeed Logic - نظام التحقق من الهوية  ")
    print("="*50)
    password = input("أدخل كلمة مرور المسؤول للدخول: ")
    
    # تشفير المدخلات ومقارنتها بالهاش المخزن
    input_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    if input_hash == ADMIN_PASSWORD_HASH:
        print("\n[✓] تم التحقق بنجاح! جاري تشغيل المحرك المحلي...\n")
        return True
    else:
        print("\n[✗] كلمة المرور غير صحيحة. تم رفض الوصول.")
        return False

def main():
    # التحقق من الأمان أولاً
    if not verify_admin():
        sys.exit(0)

    print("="*50)
    print("  تطبيق Saeed Logic - الذكاء الاصطناعي نشط الآن  ")
    print("="*50)
    print("اكتب 'خروج' أو 'exit' لإنهاء الجلسة.\n")

    engine = InferenceEngine()

    while True:
        try:
            user_input = input("أنت: ")
            if user_input.lower() in ['خروج', 'exit']:
                print("تم إغلاق نظام Saeed Logic بنجاح. في أمان الله!")
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
