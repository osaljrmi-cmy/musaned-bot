from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from typing import Tuple


def launch_browser(headless: bool = False) -> Tuple[Browser, BrowserContext, Page]:
    playwright = sync_playwright().start()

    browser = playwright.chromium.launch(
        headless=headless,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--start-maximized",
        ],
    )

    context = browser.new_context(
        viewport={"width": 1366, "height": 768},
        locale="ar-SA",
    )

    page = context.new_page()
    return browser, context, page


def close_browser(browser: Browser) -> None:
    browser.close()