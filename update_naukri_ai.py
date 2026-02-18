from playwright.sync_api import sync_playwright
from openai import OpenAI
import os
import time
import random

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key="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")


# ---------- AI HEADLINE GENERATION ----------
def generate_headline():
    prompt = """
    Generate ONE short professional Naukri resume headline (max 220 characters)
    for a Software Developer with:
    - 2+ years experience
    - Python, Backend, AI/ML interest
    - Immediate joiner
    - Recruiter-friendly keywords
    - No emojis
    - No quotation marks
    """

    response = client.responses.create(
        model="o3-mini",
        input=prompt
    )

    return response.output_text.strip()


# ---------- HUMAN-LIKE DELAY ----------
def human_delay(a=1.5, b=3.5):
    time.sleep(random.uniform(a, b))


# ---------- LOGIN FUNCTION ----------
def login_naukri(page):
    page.goto("https://www.naukri.com/nlogin/login")
    page.wait_for_load_state("networkidle")

    # Email input
    email_input = page.locator(
        'input[placeholder="Enter your active Email ID / Username"]'
    )
    email_input.wait_for(timeout=60000)
    email_input.fill(EMAIL)

    human_delay()

    # Password input
    password_input = page.locator(
        'input[placeholder="Enter your password"]'
    )
    password_input.fill(PASSWORD)

    human_delay()

    # Submit
    page.click('button[type="submit"]')

    time.sleep(10)


# ---------- UPDATE HEADLINE ----------
def update_headline(headline):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        login_naukri(page)

        # Go to profile
        page.goto("https://www.naukri.com/mnjuser/profile")
        page.wait_for_load_state("networkidle")
        time.sleep(5)

        # Click Resume Headline section
        page.locator("text=Resume Headline").first.click()
        human_delay()

        # Fill headline
        textarea = page.locator("textarea")
        textarea.wait_for(timeout=30000)
        textarea.fill(headline)

        human_delay()

        # Save
        page.locator('button:has-text("Save")').click()

        print("Updated headline:", headline)

        browser.close()


# ---------- MAIN ----------
if __name__ == "__main__":
    headline = generate_headline()
    update_headline(headline)
