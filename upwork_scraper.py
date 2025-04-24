print("✅ Script is loading...")

try:
    import os
    from dotenv import load_dotenv
    load_dotenv()
    import requests
    import time
    from playwright.sync_api import sync_playwright

    SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
    if not SLACK_WEBHOOK_URL:
        print("❌ SLACK_WEBHOOK_URL is missing! Check your Render environment variables.")
    else:
        print("✅ Slack webhook loaded")

    def load_keywords(file_path):
        print(f"📂 Loading keywords from {file_path}")
        try:
            with open(file_path, 'r') as f:
                return [line.strip().lower() for line in f if line.strip()]
        except Exception as e:
            print(f"❌ Failed to load {file_path}: {e}")
            return []

    def send_to_slack(message):
        print("📤 Sending message to Slack...")
        try:
            payload = {"text": message}
            response = requests.post(SLACK_WEBHOOK_URL, json=payload)
            print(f"✅ Slack response: {response.status_code}")
        except Exception as e:
            print("❌ Slack failed:", e)

    def scrape_upwork():
        print("👀 scrape_upwork() called")
        positive_keywords = load_keywords('positive_keywords.txt')
        negative_keywords = load_keywords('negative_keywords.txt')

        print("✅ Launching Playwright")
        with sync_playwright() as p:
            try:
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
            except Exception as e:
                print("❌ Failed to launch browser:", e)
                return

            try:
                page = browser.new_page()
                print("✅ Navigating to Upwork")
                page.goto("https://www.upwork.com/nx/jobs/search/?q=unity%20OR%20unreal&sort=recency")

                page.wait_for_selector('a[data-test="job-tile-title-link UpLink"]', timeout=20000)
                job_posts = page.query_selector_all('a[data-test="job-tile-title-link UpLink"]')
                print(f"✅ Found {len(job_posts)} job posts")

                for post in job_posts:
                    title = post.inner_text().lower()
                    href = post.get_attribute('href')
                    full_url = f"https://www.upwork.com{href}"

                    if any(pos_kw in title for pos_kw in positive_keywords) and not any(neg_kw in title for neg_kw in negative_keywords):
                        print("🎯 Match found:", title)
                        send_to_slack(f"🎯 New job matched!\n🔍 *Matched by keyword in job title*\n🔗 {full_url}")
                        break

            except Exception as e:
                print("❌ Error during scraping:", e)
            finally:
                browser.close()
                print("✅ Browser closed")

    if __name__ == "__main__":
        print("🚀 Entering main loop")
        while True:
            scrape_upwork()
            time.sleep(600)

except Exception as e:
    print("💥 Uncaught top-level error:", e)
