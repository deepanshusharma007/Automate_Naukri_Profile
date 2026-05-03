import os
import json
import requests
import dotenv

dotenv.load_dotenv()

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")

PROFILE_ID = "aa5e21de3b6391f3f347f14cabad8f6159b6139c03441d7eb679862093b973de"

HEADLINE_URL = "https://www.naukri.com/cloudgateway-mynaukri/resman-aggregator-services/v1/users/self/fullprofiles"

HEADERS = {
    "accept": "application/json",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "appid": "135",
    "clientid": "m0b5",
    "content-type": "application/json",
    "systemid": "Naukri",
    "x-http-method-override": "PUT",
    "x-requested-with": "XMLHttpRequest",
    "origin": "https://www.naukri.com",
    "referer": "https://www.naukri.com/mnj/resumeHeadline/edit?orig=ffp",
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1",
    "sec-ch-ua": '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"iOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
}

HEADLINE = "Backend Developer with 3+ years of experience in Python, API development, and AI-powered backend systems"


def get_auth_token():
    """Login to Naukri and return Bearer token + cookies."""
    print("Logging in to Naukri...")
    login_url = "https://www.naukri.com/central-login-services/v2/login"
    payload = {
        "username": EMAIL,
        "password": PASSWORD,
        "type": "login",
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "appid": "135",
        "clientid": "d3skt0p",
        "systemid": "Naukri",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    }
    session = requests.Session()
    resp = session.post(login_url, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    token = data.get("loginData", {}).get("token")
    if not token:
        raise Exception(f"Login failed: {data}")
    print("Login successful")
    return token, session.cookies


def update_headline(token, cookies):
    """Toggle a period on the headline to trigger profile update."""
    # first fetch current headline
    get_url = "https://www.naukri.com/cloudgateway-mynaukri/resman-aggregator-services/v1/users/self/fullprofiles"
    headers = {**HEADERS, "authorization": f"Bearer {token}"}

    resp = requests.get(get_url, headers=headers, cookies=cookies)
    resp.raise_for_status()
    current = resp.json().get("profile", {}).get("resumeHeadline", HEADLINE)
    print(f"Current headline: {current}")

    # toggle period
    if current.strip().endswith("."):
        new_headline = current.strip()[:-1]
    else:
        new_headline = current.strip() + "."

    print(f"Updated headline: {new_headline}")

    payload = {
        "profile": {"resumeHeadline": new_headline},
        "profileId": PROFILE_ID,
    }

    resp = requests.post(HEADLINE_URL, headers=headers, cookies=cookies, json=payload)
    resp.raise_for_status()
    print(f"Response status: {resp.status_code}")
    print("Headline updated successfully!")


def main():
    print("Starting Naukri profile update...")
    print(f"Email: {EMAIL}")

    if not EMAIL or not PASSWORD:
        raise Exception("NAUKRI_EMAIL and NAUKRI_PASSWORD must be set")

    token, cookies = get_auth_token()
    update_headline(token, cookies)


if __name__ == "__main__":
    main()
