import requests
import json
import os
from datetime import datetime

CONFIG_FILE = "companies.json"

def format_application(app):
    """Extract and format only the meaningful fields."""

    title = app.get("postingTitle", "Unknown Title")
    requisition = app.get("jobRequisitionId", "N/A")
    status = app.get("status", "Unknown")
    applied_on = app.get("dateApplied", "Unknown Date")

    return (
        f"Job Title: {title}\n"
        f"Requisition: {requisition}\n"
        f"Status: {status}\n"
        f"Applied On: {applied_on}\n"
        "------------------------------\n"
    )

def append_to_file(company, apps):
    filename = f"{company}.txt"
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"\n\n===== {timestamp} =====\n\n")

        for app in apps:
            f.write(format_application(app))

def build_url(comp):
    base_url = comp["base_url"]
    app_type = comp.get("type", "active")
    limit = comp.get("limit", 20)

    return f"{base_url}?type={app_type}&limit={limit}"

def main():
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

    for comp in config["companies"]:
        name = comp["name"]
        url = build_url(comp)

        cookie = os.getenv(comp["cookie_secret"])
        csrf = os.getenv(comp["csrf_secret"])

        if not cookie or not csrf:
            print(f"[WARN] Missing secrets for {name}, skipping...")
            continue

        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "x-calypso-csrf-token": csrf,
            "Cookie": cookie
        }

        print(f"[INFO] Fetching for {name}...")

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            apps = data.get("data", [])

            append_to_file(name, apps)
            print(f"[OK] Saved formatted data to {name}.txt")

        except Exception as e:
            print(f"[ERROR] Failed for {name}: {e}")

if __name__ == "__main__":
    main()
