def answer(self, user_input):
    try:
        # التأكد من وجود مجلد البيانات
        memory_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        if not os.path.exists(memory_dir):
            os.makedirs(memory_dir, exist_ok=True)
            
        # تحميل الذاكرة الحالية
        memory_file = os.path.join(memory_dir, "memory.json")
        if os.path.exists(memory_file):
            with open(memory_file, 'r', encoding='utf-8') as f:
                self.memory = json.load(f)
        
        # معالجة الإدخال
        response = self.process_input(user_input)
        
        # تحديث الذاكرة
        self.memory[user_input] = response
        
        # حفظ الذاكرة
        save_json(memory_file, self.memory)
        
        return response
        
    except Exception as e:
        print(f"خطأ في معالجة السؤال: {e}")
        return "حدث خطأ أثناء معالجة سؤالك. يرجى المحاولة مرة أخرى."
