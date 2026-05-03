from playwright.sync_api import sync_playwright
import os
import time
import random
import dotenv

dotenv.load_dotenv()

EMAIL = os.getenv("NAUKRI_EMAIL")
print("Using email:", EMAIL)

PASSWORD = os.getenv("NAUKRI_PASSWORD")
print("Using password:", "********" if PASSWORD else "None")


# ---------- HUMAN-LIKE DELAY ----------
def human_delay(a=1.2, b=2.8):
    time.sleep(random.uniform(a, b))


def scroll_page(page):
    """Force profile sections to load"""
    for _ in range(10):
        page.evaluate("window.scrollBy(0, 1000)")
        time.sleep(1)


# ---------- UPDATE HEADLINE ----------
def update_headline():

    print("Starting Naukri automation...")
    print("Files:", os.listdir())
    print("auth.json exists:", os.path.exists("auth.json"))

    with sync_playwright() as p:

        browser = p.chromium.launch(
            channel="chrome",  # use real installed Chrome, not Playwright's Chromium
            headless=False,    # headless=False avoids many bot-detection triggers
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--start-maximized",
            ]
        )

        context = browser.new_context(
            storage_state="auth.json" if os.path.exists("auth.json") else None,
            viewport=None,  # let Chrome use its natural window size
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        )

        # mask automation signals
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.chrome = { runtime: {} };
        """)

        page = context.new_page()

        # open profile
        page.goto("https://www.naukri.com/mnjuser/profile", timeout=60000)

        page.wait_for_load_state("domcontentloaded")
        time.sleep(5)

        print("Current URL:", page.url)

        # if redirected to login, session expired — do a fresh login
        if "login" in page.url or "naukri.com/mnjuser/profile" not in page.url:
            print("Session expired, logging in...")
            if not EMAIL or not PASSWORD:
                raise Exception("Session expired and no credentials provided")
            page.goto("https://www.naukri.com/nlogin/login", timeout=60000)
            page.wait_for_load_state("domcontentloaded")
            page.locator("input[placeholder='Enter your active Email ID / Username']").fill(EMAIL)
            human_delay(0.5, 1.2)
            page.locator("input[placeholder='Enter your password']").fill(PASSWORD)
            human_delay(0.5, 1.2)
            page.get_by_role("button", name="Login").click()
            page.wait_for_load_state("domcontentloaded")
            time.sleep(4)
            print("Logged in, now navigating to profile...")
            page.goto("https://www.naukri.com/mnjuser/profile", timeout=60000)
            page.wait_for_load_state("domcontentloaded")
            time.sleep(5)
            print("Current URL after login:", page.url)

        # debug screenshot
        page.screenshot(path="debug_profile_page.png", full_page=True)

        # scroll page to load all widgets
        print("Scrolling page to trigger lazy loading")
        scroll_page(page)

        # ---------- OPEN EDIT MODAL ----------
        print("Searching for edit icon")

        # dump page HTML for debugging selector issues
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(page.content())

        # try multiple selectors in case Naukri changed their markup
        selectors = [
            "span.edit.icon",
            "span[class*='edit']",
            "button[class*='edit']",
            "[data-ga-track*='resumeHeadline'] span[class*='edit']",
            "div.widgetHead span.edit",
            "span.editIcon",
        ]

        edit_button = None
        for sel in selectors:
            loc = page.locator(sel)
            if loc.count() > 0:
                edit_button = loc.nth(0)
                print(f"Found edit button with selector: {sel}")
                break

        if edit_button is None:
            page.screenshot(path="no_edit_icon.png", full_page=True)
            raise Exception("No edit icons found on profile page — check no_edit_icon.png and page_source.html")

        edit_button.click()

        print("Clicked edit icon")

        # ---------- TEXTAREA ----------
        textarea = page.locator("#resumeHeadlineTxt")

        textarea.wait_for(timeout=60000)

        current_text = textarea.input_value().strip()

        print("Current headline:", current_text)

        # toggle period
        if current_text.endswith("."):
            new_text = current_text[:-1]
        else:
            new_text = current_text + "."

        print("Updated headline:", new_text)

        textarea.fill(new_text)

        human_delay()

        # ---------- SAVE ----------
        save_button = page.get_by_role("button", name="Save")

        save_button.wait_for(timeout=60000)
        save_button.click()

        print("Headline updated successfully")

        page.screenshot(path="headline_updated.png", full_page=True)

        browser.close()


# ---------- MAIN ----------
if __name__ == "__main__":
    update_headline()
