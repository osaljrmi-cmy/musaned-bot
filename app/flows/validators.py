def is_cancel(text: str) -> bool:
    return text.strip() == "إلغاء"

def is_yes(text: str) -> bool:
    t = text.strip().lower()
    return t in ["نعم", "✅ نعم", "yes", "y"]

def is_no(text: str) -> bool:
    t = text.strip().lower()
    return t in ["لا", "❌ لا", "no", "n"]

def parse_choice(text: str):
    t = text.strip()
    if t.isdigit():
        n = int(t)
        if 1 <= n <= 5:
            return n
    return None
