from playwright.sync_api import sync_playwright
from openai import OpenAI
import os
import time
import random
import dotenv

dotenv.load_dotenv()

EMAIL = os.getenv("NAUKRI_EMAIL")
print("Using email:", EMAIL)

PASSWORD = os.getenv("NAUKRI_PASSWORD")
print("Using password:", "********" if PASSWORD else "None")

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# client = OpenAI(api_key=<YOUR_API_KEY>)


# # ---------- AI HEADLINE GENERATION ----------
# def generate_headline():
#     prompt = """
# Generate ONE short professional Naukri resume headline (max 220 characters)
# for a Software Developer with:
# - 2+ years experience
# - Python, Backend, AI/ML interest
# - Immediate joiner
# - Recruiter-friendly keywords
# - No emojis
# - No quotation marks
# """

#     response = client.responses.create(
#         model="o3-mini",
#         input=prompt
#     )

#     return response.output_text.strip()


# ---------- HUMAN-LIKE DELAY ----------
def human_delay(a=1.2, b=2.8):
    time.sleep(random.uniform(a, b))


# ---------- LOGIN ----------
def login_naukri(page):
    # Go directly to login page (simplest & most reliable)
    page.goto("https://login.naukri.com/nLogin/Login.php", timeout=60000)

    # Click Login link in header
    # page.locator('#login_Layer').click()

    # ----- Email -----
    email_input = page.locator(
        'input[placeholder="Enter Email ID / Username"]'
    )
    email_input.wait_for(timeout=60000)
    email_input.fill(EMAIL)

    human_delay()

    # ----- Password -----
    password_input = page.locator(
        'input[placeholder="Enter Password"]'
    )
    password_input.fill(PASSWORD)

    human_delay()

    # ----- Login Button -----
    # page.locator('button.Login').click()
    page.get_by_role("button", name="Login", exact=True).click()

    print("Clicked Login button")


# ---------- UPDATE HEADLINE ----------
def update_headline():

    with sync_playwright() as p:

        # browser = p.chromium.launch(headless=False)

        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )

        # load saved session
        context = browser.new_context(storage_state="auth.json")

        page = context.new_page()

        # LOGIN
        # login_naukri(page)

        # navigate directly to profile page using saved session
        page.goto("https://www.naukri.com/mnjuser/profile", timeout=60000)

        # Wait for navigation after login
        page.wait_for_load_state("domcontentloaded")
        time.sleep(2)

        print("After login URL:", page.url)

        try:
            profile_link = page.locator('a[href="/mnjuser/profile"]')
            profile_link.wait_for(timeout=15000)
            profile_link.click()
            print("Navigated to profile via header link")
        except:
            print("Profile link not found — using direct navigation")
            page.goto("https://www.naukri.com/mnjuser/profile")

        # Wait for profile page
        page.wait_for_load_state("domcontentloaded")
        time.sleep(2)

        print("Current URL:", page.url)

        # Locate Resume Headline section
        headline_section = page.locator(
            "div.widgetHead:has-text('Resume headline')"
        )

        headline_section.wait_for(timeout=60000)

        # Scroll to it (works with nested containers)
        headline_section.scroll_into_view_if_needed()

        # time.sleep(3)

        # Click pencil icon inside it
        edit_button = headline_section.locator("span.edit.icon")
        edit_button.click()

        print("Clicked Resume Headline edit icon")

        # Locate textarea
        textarea = page.locator("#resumeHeadlineTxt")

        textarea.wait_for(timeout=60000)

        # Get current text
        current_text = textarea.input_value().strip()

        print("Current headline:", current_text)

        # Toggle final period
        if current_text.endswith("."):
            new_text = current_text[:-1]  # remove period
        else:
            new_text = current_text + "."  # add period

        print("Updated headline:", new_text)

        # Update textarea
        textarea.fill(new_text)

        # page.get_by_role("button", name="Save").click()
        # Click Save
        save_button = page.get_by_role("button", name="Save")
        save_button.wait_for(timeout=60000)
        save_button.click()

        print("Headline updated successfully")

        browser.close()


# ---------- MAIN ----------
if __name__ == "__main__":
    # headline = generate_headline()
    update_headline()
