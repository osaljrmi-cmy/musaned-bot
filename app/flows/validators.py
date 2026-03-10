import re


def is_cancel(text: str) -> bool:
    t = text.strip().lower()
    return t in ["إلغاء", "الغاء", "cancel"]


def is_yes(text: str) -> bool:
    t = text.strip().lower()
    return t in ["نعم", "1", "yes", "y"]


def is_no(text: str) -> bool:
    t = text.strip().lower()
    return t in ["لا", "2", "no", "n"]


def parse_choice(text: str):
    t = text.strip()
    if t.isdigit():
        n = int(t)
        if 1 <= n <= 6:
            return n
    return None


def is_done(text: str) -> bool:
    t = text.strip().lower()
    return t in ["تم", "done", "ok"]


def parse_otp_command(text: str):
    t = text.strip()
    m = re.match(r"^(?:رمز|otp)\s+(\d{4,8})$", t, flags=re.IGNORECASE)
    if m:
        return m.group(1)
    return None