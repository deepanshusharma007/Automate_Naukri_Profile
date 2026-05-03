import os
import json
import requests
import dotenv

dotenv.load_dotenv()

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")

PROFILE_ID = "aa5e21de3b6391f3f347f14cabad8f6159b6139c03441d7eb679862093b973de"
HEADLINE_URL = "https://www.naukri.com/cloudgateway-mynaukri/resman-aggregator-services/v1/users/self/fullprofiles"
LOGIN_URL = "https://www.naukri.com/central-login-services/v1/login"

COMMON_HEADERS = {
    "accept": "application/json",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "appid": "135",
    "clientid": "m0b5",
    "content-type": "application/json",
    "origin": "https://www.naukri.com",
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1",
    "sec-ch-ua": '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"iOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest",
}


def login():
    """Login and return Bearer token + session cookies."""
    print(f"Logging in as {EMAIL}...")
    session = requests.Session()
    resp = session.post(
        LOGIN_URL,
        headers={**COMMON_HEADERS, "systemid": "jobseeker", "referer": "https://www.naukri.com/mnj/login"},
        json={"username": EMAIL, "password": PASSWORD, "isLoginByEmail": True},
    )
    print(f"Login response: {resp.status_code}")
    resp.raise_for_status()
    data = resp.json()
    print(f"Login data keys: {list(data.keys())}")

    # token can be in different places depending on response structure
    token = (
        data.get("loginData", {}).get("token")
        or data.get("data", {}).get("token")
        or data.get("token")
        or session.cookies.get("nauk_at")
    )

    if not token:
        raise Exception(f"Could not find token in login response: {json.dumps(data, indent=2)[:500]}")

    print("Login successful")
    return token, session.cookies


def update_headline(token, cookies):
    """Fetch current headline, toggle period, save."""
    headers = {
        **COMMON_HEADERS,
        "authorization": f"Bearer {token}",
        "systemid": "Naukri",
        "referer": "https://www.naukri.com/mnj/resumeHeadline/edit?orig=ffp",
        "x-http-method-override": "PUT",
    }

    # fetch current headline
    resp = requests.get(HEADLINE_URL, headers=headers, cookies=cookies)
    resp.raise_for_status()
    current = resp.json().get("profile", {}).get("resumeHeadline", "")
    print(f"Current headline: {current}")

    if not current:
        raise Exception("Could not fetch current headline")

    new_headline = current.strip()[:-1] if current.strip().endswith(".") else current.strip() + "."
    print(f"Updated headline: {new_headline}")

    resp = requests.post(
        HEADLINE_URL,
        headers=headers,
        cookies=cookies,
        json={"profile": {"resumeHeadline": new_headline}, "profileId": PROFILE_ID},
    )
    resp.raise_for_status()
    print(f"Save response: {resp.status_code}")
    print("Headline updated successfully!")


def main():
    print("Starting Naukri profile update...")
    if not EMAIL or not PASSWORD:
        raise Exception("NAUKRI_EMAIL and NAUKRI_PASSWORD must be set as env vars or in .env")
    token, cookies = login()
    update_headline(token, cookies)


if __name__ == "__main__":
    main()
