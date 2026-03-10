import os
from dotenv import load_dotenv
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from app.musaned.browser import launch_browser, close_browser
from app.musaned.constants import (
    CAPTCHA_REQUIRED,
    LOGIN_FAILED,
    LOGIN_BUTTON_NOT_FOUND,
    LOGIN_FIELDS_NOT_FOUND,
    LOGIN_SUCCESS,
    OTP_REQUIRED,
)

load_dotenv()

MUSANED_URL = "https://tawtheeq.musaned.com.sa/"


def login_to_musaned(headless: bool = False) -> str:
    username = os.getenv("MUSANED_USERNAME")
    password = os.getenv("MUSANED_PASSWORD")

    if not username or not password:
        raise RuntimeError("MUSANED_USERNAME or MUSANED_PASSWORD is not set")

    browser, context, page = launch_browser(headless=headless)

    try:
        print("[musaned] opening page", flush=True)
        page.goto(MUSANED_URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(3000)

        print("[musaned] clicking login button", flush=True)

        login_clicked = False

        login_button_selectors = [
            "button:has-text('تسجيل الدخول')",
            "a:has-text('تسجيل الدخول')",
            "text=تسجيل الدخول",
        ]

        for selector in login_button_selectors:
            try:
                locator = page.locator(selector)
                if locator.count() > 0:
                    locator.first.click(force=True)
                    login_clicked = True
                    print(f"[musaned] login clicked using: {selector}", flush=True)
                    break
            except Exception:
                continue

        if not login_clicked:
            page.screenshot(path="musaned_no_login_button.png", full_page=True)
            return LOGIN_BUTTON_NOT_FOUND

        print("[musaned] waiting for login fields", flush=True)
        page.wait_for_timeout(4000)

        username_ready = False
        password_ready = False
        username_selector = None
        password_selector = None

        username_selectors = [
            "#jwda",
            'input[placeholder*="اسم المستخدم"]',
            'input[placeholder*="البريد"]',
            'input[type="text"]',
        ]

        password_selectors = [
            "#jwdamal",
            'input[type="password"]',
        ]

        for selector in username_selectors:
            try:
                page.locator(selector).first.wait_for(state="visible", timeout=10000)
                username_selector = selector
                username_ready = True
                print(f"[musaned] username selector found: {selector}", flush=True)
                break
            except Exception:
                continue

        for selector in password_selectors:
            try:
                page.locator(selector).first.wait_for(state="visible", timeout=10000)
                password_selector = selector
                password_ready = True
                print(f"[musaned] password selector found: {selector}", flush=True)
                break
            except Exception:
                continue

        if not username_ready or not password_ready:
            page.screenshot(path="musaned_login_fields_not_found.png", full_page=True)
            with open("musaned_login_fields_not_found.html", "w", encoding="utf-8") as f:
                f.write(page.content())
            return LOGIN_FIELDS_NOT_FOUND

        print("[musaned] filling username", flush=True)
        page.locator(username_selector).first.fill(username)

        print("[musaned] filling password", flush=True)
        page.locator(password_selector).first.fill(password)

        page.screenshot(path="musaned_login_form_filled.png", full_page=True)

        page_content = page.content().lower()
        if "recaptcha" in page_content or "g-recaptcha" in page_content:
            print("[musaned] captcha detected before submit", flush=True)
            page.screenshot(path="musaned_captcha_detected.png", full_page=True)
            return CAPTCHA_REQUIRED

        print("[musaned] submitting form", flush=True)

        if page.locator("button[type='submit']").count() > 0:
            page.locator("button[type='submit']").first.click()
        else:
            page.keyboard.press("Enter")

        page.wait_for_timeout(6000)

        current_url = page.url
        current_content = page.content().lower()

        print(f"[musaned] current url: {current_url}", flush=True)

        if "otp" in current_content or "verification" in current_content or "رمز" in current_content:
            page.screenshot(path="musaned_otp_detected.png", full_page=True)
            return OTP_REQUIRED

        if "recaptcha" in current_content or "g-recaptcha" in current_content:
            page.screenshot(path="musaned_captcha_after_submit.png", full_page=True)
            return CAPTCHA_REQUIRED

        if "dashboard" in current_url or "home" in current_url:
            page.screenshot(path="musaned_login_success.png", full_page=True)
            return LOGIN_SUCCESS

        page.screenshot(path="musaned_after_submit_unknown.png", full_page=True)
        return LOGIN_FAILED

    except PlaywrightTimeoutError as e:
        print(f"[musaned] timeout: {e}", flush=True)
        page.screenshot(path="musaned_timeout.png", full_page=True)
        return LOGIN_FAILED

    finally:
        close_browser(browser)