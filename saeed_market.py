# =====================================================================
# 3. محرك الذكاء المرتبط بـ Gemini SDK
# =====================================================================
def get_gemini_smart_response(user_input):
    """
    ترسل أي نص يكتبه المستخدم مباشرة إلى خوارزميات Gemini الذكية،
    وتستقبل رداً متكاملاً، وتولد له ملفاً صوتياً فورياً.
    """
    if not user_input or user_input.strip() == "":
        user_input = "مرحباً"

    # 🎯 تعليمات النظام وقاعدة معرفة الكوبونات والعروض
    system_instruction = """
أنت مساعد التسوق الذكي لـ Saeed MarketAds. 
وظيفتك الأساسية هي إعطاء كود الخصم فوراً ورابط العرض بشكل مباشر وواضح للمستخدم دون إعطاء نصائح عامة أو إجابات عائمة.

قائمة الأكواد والعروض المتاحة حالياً:
1. متجر SHEIN (شي إن):
   - كود الخصم: Saeed15
   - التفاصيل: خصم 15% على جميع المنتجات.
2. متجر نون (Noon):
   - كود الخصم: SaeedNoon
   - التفاصيل: خصم إضافي + توصيل مجاني.
3. متجر علي إكسبريس (AliExpress):
   - كود الخصم: SaeedAE
   - التفاصيل: عروض مباشرة وخصومات على الشحن.

عندما يطلب المستخدم كود خصم أو عرض لأي متجر:
- أعطه الكود فوراً وبخط بارز (Bold) ومباشر.
- اذكر نسبة الخصم والتفاصيل فوراً.
"""

    try:
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.3,  # درجة حرارة منخفضة لضمان الدقة وعدم التخمين
            top_p=0.95,
            max_output_tokens=1024,
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_input,
            config=config,
        )
        reply_text = response.text.strip()

    except Exception as e:
        print("=== ERROR IN GEMINI GENERATION ===")
        traceback.print_exc()
        reply_text = f"أهلاً بك يا سعيد. عذراً واجهتني مشكلة بسيطة في الاتصال بالسيرفر ({e})، لكننا مستمرون تحت راية Saeed MarketAds!"

    # توليد الصوت للرد الناتج تلقائياً
    try:
        generate_audio_file(reply_text)
    except Exception as e:
        print(f"Audio generation skipped due to error: {e}")
    
    return reply_text
