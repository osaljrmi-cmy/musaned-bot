def menu_text() -> str:
    return (
        ""اختر العملية المطلوبة بإرسال رقمها:\\n\\n""
        ""1) إضافة مرشح\\n""
        ""2) حذف مرشح\\n""
        ""3) موافقة عقد ارتباط\\n""
        ""4) موافقة إلغاء عقد ارتباط\\n""
        ""5) رفع عقد مساند""
    )

def invalid_choice() -> str:
    return ""اختيار غير صحيح. أرسل رقم من 1 إلى 5.""

def send_image_first_note() -> str:
    return ""📷 تم استلام الصورة.\\n"" + menu_text()

def next_action_prompt() -> str:
    return ""هل تريد تنفيذ عملية أخرى؟\\n✅ نعم\\n❌ لا""

def ended() -> str:
    return ""✅ تم إنهاء الجلسة. أرسل صورة لبدء عملية جديدة.""

def busy() -> str:
    return ""⏳ توجد عملية قيد التنفيذ الآن. انتظر حتى تنتهي أو اكتب (إلغاء).""

def cancelled() -> str:
    return ""✅ تم إلغاء العملية.""

def ask_send_image() -> str:
    return ""أرسل صورة لبدء العملية.""
