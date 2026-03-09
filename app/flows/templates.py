def menu_text() -> str:
    return (
        "اختر العملية المطلوبة بإرسال رقمها:\n\n"
        "1) استخراج بيانات الجواز\n"
        "2) استبدال الصورة\n"
        "3) إنهاء الجلسة"
    )


def invalid_choice() -> str:
    return "اختيار غير صحيح. أرسل رقمًا من 1 إلى 3."


def send_image_first_note() -> str:
    return (
        "📷 تم استلام الصورة بنجاح.\n\n"
        "يمكنك الآن اختيار العملية المطلوبة:\n\n"
        f"{menu_text()}"
    )


def next_action_prompt() -> str:
    return (
        "هل تريد تنفيذ عملية أخرى؟\n\n"
        "1) نعم\n"
        "2) لا"
    )


def ended() -> str:
    return (
        "تم إنهاء الجلسة.\n"
        "أرسل صورة جواز جديدة لبدء عملية أخرى."
    )


def busy() -> str:
    return (
        "توجد عملية قيد التنفيذ الآن.\n"
        "انتظر حتى تنتهي أو اكتب (إلغاء)."
    )


def cancelled() -> str:
    return "تم إلغاء العملية."


def ask_send_image() -> str:
    return "أرسل صورة الجواز لبدء العملية."


def no_image_yet() -> str:
    return "لا توجد صورة محفوظة حاليًا. أرسل صورة الجواز أولًا."


def extracting_passport() -> str:
    return "جاري تجهيز استخراج بيانات الجواز من الصورة..."


def passport_extraction_not_ready() -> str:
    return (
        "تم استلام طلب استخراج البيانات.\n"
        "مرحلة الاستخراج الفعلي من الصورة سنفعّلها في الخطوة التالية."
    )


def replace_image_prompt() -> str:
    return "أرسل صورة جديدة لاستبدال الصورة الحالية."


def session_summary_after_choice(choice: int) -> str:
    if choice == 1:
        return "تم اختيار: استخراج بيانات الجواز."
    if choice == 2:
        return "تم اختيار: استبدال الصورة."
    if choice == 3:
        return "تم اختيار: إنهاء الجلسة."
    return "تم اختيار العملية."