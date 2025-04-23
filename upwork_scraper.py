import os
from dotenv import load_dotenv
load_dotenv()
import requests
import time
from playwright.sync_api import sync_playwright

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


def load_keywords(file_path):
    with open(file_path, 'r') as f:
        return [line.strip().lower() for line in f if line.strip()]

def send_to_slack(message):
    payload = {"text": message}
    requests.post(SLACK_WEBHOOK_URL, json=payload)

def scrape_upwork():
    positive_keywords = load_keywords('positive_keywords.txt')
    negative_keywords = load_keywords('negative_keywords.txt')

    print("✅ Launching Playwright")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--disable-setuid-sandbox",
                "--disable-extensions",
                "--disable-infobars",
                "--window-size=1920,1080",
                "--use-gl=swiftshader"
            ]
        )
        print("✅ Browser launched")

        page = browser.new_page()
        page.goto("https://www.upwork.com/nx/jobs/search/?q=unity%20OR%20unreal&sort=recency")

        try:
            page.wait_for_selector('a[data-test="job-tile-title-link UpLink"]', timeout=20000)
        except:
            print("❌ Job titles not found — skipping this run.")
            browser.close()
            return

        job_posts = page.query_selector_all('a[data-test="job-tile-title-link UpLink"]')
        for post in job_posts:
            title = post.inner_text().lower()
            href = post.get_attribute('href')
            full_url = f"https://www.upwork.com{href}"

            if any(pos_kw in title for pos_kw in positive_keywords) and not any(neg_kw in title for neg_kw in negative_keywords):
                send_to_slack(f"🎯 New job matched!\n🔍 *Matched by keyword in job title*\n🔗 {full_url}")
                break

        browser.close()

if __name__ == "__main__":
    while True:
        scrape_upwork()
        time.sleep(600)  # Check every 10 minutes
