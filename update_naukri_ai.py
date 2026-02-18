from playwright.sync_api import sync_playwright
from openai import OpenAI
import os
import time
import random

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


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

    headline = response.output_text.strip()
    return headline


# ---------- HUMAN-LIKE DELAY ----------
def human_delay(a=1.5, b=3.5):
    time.sleep(random.uniform(a, b))


# ---------- NAUKRI UPDATE ----------
def update_headline(headline):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Login
        page.goto("https://www.naukri.com/nlogin/login")
        human_delay()

        page.fill('input[type="text"]', EMAIL)
        human_delay()

        page.fill('input[type="password"]', PASSWORD)
        human_delay()

        page.click('button[type="submit"]')

        time.sleep(8)

        # Profile page
        page.goto("https://www.naukri.com/mnjuser/profile")
        time.sleep(8)

        # Edit Resume Headline
        page.click('text=Resume Headline')
        human_delay()

        textarea = page.locator("textarea")
        textarea.fill(headline)
        human_delay()

        page.click('button:has-text("Save")')

        print("Updated headline:", headline)

        browser.close()


# ---------- MAIN ----------
if __name__ == "__main__":
    headline = generate_headline()
    update_headline(headline)
