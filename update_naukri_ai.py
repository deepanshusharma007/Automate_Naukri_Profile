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


# ---------- UPDATE HEADLINE ----------
def update_headline():

    print("Starting Naukri automation...")
    print("Files in working directory:", os.listdir())
    print("auth.json exists:", os.path.exists("auth.json"))

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )

        # use stored login session
        context = browser.new_context(
            storage_state="auth.json",
            viewport={"width": 1280, "height": 900}
        )

        page = context.new_page()

        # go directly to profile page
        page.goto("https://www.naukri.com/mnjuser/profile", timeout=60000)

        page.wait_for_load_state("domcontentloaded")
        time.sleep(3)

        print("Current URL:", page.url)

        # debug screenshot
        page.screenshot(path="debug_profile_page.png", full_page=True)

        # ---------- Locate Resume Headline Widget ----------
        # This selector targets the container that has Resume headline
        headline_widget = page.locator(
            "div.widgetHead:has(span.widgetTitle:has-text('Resume headline'))"
        )

        headline_widget.wait_for(timeout=60000)

        print("Resume headline widget located")

        # click edit icon inside this widget
        edit_button = headline_widget.locator("span.edit.icon")

        edit_button.wait_for(timeout=60000)
        edit_button.click()

        print("Clicked Resume Headline edit icon")

        # ---------- Locate textarea ----------
        textarea = page.locator("#resumeHeadlineTxt")

        textarea.wait_for(timeout=60000)

        # get current headline
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

        # ---------- Click Save ----------
        save_button = page.get_by_role("button", name="Save")

        save_button.wait_for(timeout=60000)
        save_button.click()

        print("Headline updated successfully")

        # screenshot after update
        page.screenshot(path="headline_updated.png", full_page=True)

        browser.close()


# ---------- MAIN ----------
if __name__ == "__main__":
    update_headline()
