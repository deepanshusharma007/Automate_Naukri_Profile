import os
import json
import requests
import dotenv

dotenv.load_dotenv()

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


def load_auth_from_file():
    """Load Bearer token and cookies from auth.json (Playwright session file)."""
    with open("auth.json") as f:
        state = json.load(f)

    cookies = {c["name"]: c["value"] for c in state.get("cookies", [])}
    token = cookies.get("nauk_at")

    if not token:
        raise Exception("nauk_at token not found in auth.json — regenerate auth.json")

    print("Loaded auth from auth.json")
    return token, cookies


def update_headline(token, cookies):
    """Fetch current headline, toggle period, and save."""
    headers = {**HEADERS, "authorization": f"Bearer {token}"}

    # fetch current headline
    resp = requests.get(HEADLINE_URL, headers=headers, cookies=cookies)
    resp.raise_for_status()
    data = resp.json()
    current = data.get("profile", {}).get("resumeHeadline", "")
    print(f"Current headline: {current}")

    if not current:
        raise Exception("Could not fetch current headline from API")

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
    print(f"Response: {resp.status_code}")
    print("Headline updated successfully!")


def main():
    print("Starting Naukri profile update...")
    token, cookies = load_auth_from_file()
    update_headline(token, cookies)


if __name__ == "__main__":
    main()
