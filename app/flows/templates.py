def menu_text() -> str:
    return (
        "📌 اختر العملية المطلوبة بإرسال رقمها:\n\n"
        "1) إضافة مرشح\n"
        "2) حذف مرشح\n"
        "3) موافقة عقد ارتباط\n"
        "4) موافقة إلغاء عقد ارتباط\n"
        "5) رفع عقد مساند\n"
        "6) استخراج بيانات الجواز فقط"
    )


def invalid_choice() -> str:
    return "اختيار غير صحيح. أرسل رقمًا من 1 إلى 6."


def send_image_first_note() -> str:
    return (
        "📷 تم استلام صورة الجواز بنجاح.\n\n"
        f"{menu_text()}"
    )


def next_action_prompt() -> str:
    return "هل تريد تنفيذ عملية أخرى؟\n\n1) نعم\n2) لا"


def ended() -> str:
    return "تم إنهاء الجلسة.\nأرسل صورة جواز جديدة لبدء عملية أخرى."


def busy() -> str:
    return "توجد عملية قيد التنفيذ الآن.\nانتظر حتى تنتهي أو اكتب (إلغاء)."


def cancelled() -> str:
    return "تم إلغاء العملية."


def ask_send_image() -> str:
    return "أرسل صورة الجواز لبدء العملية."


def no_image_yet() -> str:
    return "لا توجد صورة محفوظة حاليًا. أرسل صورة الجواز أولًا."


def extracting_passport() -> str:
    return "جاري تجهيز استخراج بيانات الجواز من الصورة..."


def passport_extraction_not_ready() -> str:
    return "تم حفظ الطلب. مرحلة الاستخراج الفعلي من الصورة سنفعّلها في الخطوة التالية."


def replace_image_prompt() -> str:
    return "أرسل صورة جواز جديدة لاستبدال الصورة الحالية."


def session_summary_after_choice(choice: int) -> str:
    mapping = {
        1: "تم اختيار: إضافة مرشح.",
        2: "تم اختيار: حذف مرشح.",
        3: "تم اختيار: موافقة عقد ارتباط.",
        4: "تم اختيار: موافقة إلغاء عقد ارتباط.",
        5: "تم اختيار: رفع عقد مساند.",
        6: "تم اختيار: استخراج بيانات الجواز فقط.",
    }
    return mapping.get(choice, "تم اختيار العملية.")


def musaned_session_expired() -> str:
    return (
        "⚠️ جلسة مساند غير جاهزة.\n"
        "سيتم بدء محاولة تسجيل الدخول تلقائيًا."
    )


def musaned_captcha_required() -> str:
    return (
        "⚠️ تم الوصول إلى صفحة تسجيل الدخول في مساند.\n"
        "تم إدخال اسم المستخدم وكلمة المرور.\n"
        "يلزم حل الكابتشا من طرف المشرف.\n"
        "تم حفظ العملية مؤقتًا حتى استكمال التحقق."
    )


def musaned_otp_required() -> str:
    return (
        "⚠️ تم تجاوز خطوة تسجيل الدخول الأولى في مساند.\n"
        "يلزم إدخال رمز التحقق (OTP) لإكمال الدخول.\n"
        "تم حفظ العملية مؤقتًا حتى استكمال التحقق."
    )


def musaned_login_failed() -> str:
    return (
        "❌ تعذر تسجيل الدخول إلى مساند.\n"
        "يرجى التحقق من الجلسة أو بيانات الدخول ثم إعادة المحاولة."
    )


def musaned_session_ready() -> str:
    return "✅ جلسة مساند جاهزة، سيتم تنفيذ العملية."


def supervisor_captcha_message(employee_wa_id: str, operation: int | None) -> str:
    return (
        "🔐 مطلوب تدخل المشرف في مساند.\n\n"
        f"الموظف: {employee_wa_id}\n"
        f"العملية: {operation}\n"
        "الحالة: كابتشا\n\n"
        "بعد حل الكابتشا أرسل:\n"
        "تم"
    )


def supervisor_otp_message(employee_wa_id: str, operation: int | None) -> str:
    return (
        "🔐 مطلوب رمز تحقق لمساند.\n\n"
        f"الموظف: {employee_wa_id}\n"
        f"العملية: {operation}\n"
        "الحالة: OTP\n\n"
        "أرسل الرمز بهذه الصيغة:\n"
        "رمز 123456"
    )


def supervisor_done_ack() -> str:
    return "تم استلام تأكيد المشرف. سنكمل ربط الاستئناف في الخطوة التالية."


def supervisor_otp_ack(code: str) -> str:
    return f"تم استلام رمز التحقق: {code}. سنكمل ربط الاستئناف في الخطوة التالية."


def no_pending_supervisor_action() -> str:
    return "لا توجد عملية معلقة حاليًا بانتظار المشرف."