

import os
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


MUSANED_URL = "https://tawtheeq.musaned.com.sa/"


def login_to_musaned(headless=True):

    username = os.getenv("MUSANED_USERNAME")
    password = os.getenv("MUSANED_PASSWORD")

    if not username or not password:
        raise RuntimeError("MUSANED_USERNAME or MUSANED_PASSWORD is not set")

    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu"
            ]
        )

        context = browser.new_context()
        page = context.new_page()

        print("[musaned] opening page")

        page.goto(MUSANED_URL)

        print("[musaned] clicking login button")

        try:
            page.locator("button:has-text('تسجيل الدخول')").click()
        except:
            page.locator("a:has-text('تسجيل الدخول')").click()

        print("[musaned] waiting for login fields")

        page.wait_for_selector("input[type='text']")
        page.wait_for_selector("input[type='password']")

        print("[musaned] filling username")
        page.locator("input[type='text']").fill(username)

        print("[musaned] filling password")
        page.locator("input[type='password']").fill(password)

        if page.locator("iframe[src*='recaptcha']").count() > 0:
            print("[musaned] captcha detected before submit")
            return "CAPTCHA_REQUIRED"

        print("[musaned] submitting login")

        page.locator("button:has-text('تسجيل الدخول')").click()

        try:
            page.wait_for_timeout(5000)
        except PlaywrightTimeoutError:
            pass

        print("[musaned] login attempt done")

        return "LOGIN_ATTEMPTED"