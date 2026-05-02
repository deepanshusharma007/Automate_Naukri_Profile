from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto('https://www.naukri.com/nlogin/login')
    input('Log in manually in the browser, then press Enter here...')
    context.storage_state(path='auth.json')
    print('auth.json saved!')
    browser.close()