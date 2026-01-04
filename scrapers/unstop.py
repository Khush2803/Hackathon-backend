from playwright.sync_api import sync_playwright
from datetime import datetime
import time

def fetch_unstop_hackathons(max_pages=5):
    
    hackathons = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for page_num in range(1, max_pages + 1):
            url = f"https://unstop.com/hackathons?page={page_num}"
            print(f"🔹 Scraping Unstop page {page_num}: {url}")

            try:
                page.goto(url, timeout=60000)
                # Wait for at least one hackathon listing
                page.wait_for_selector("app-competition-listing a.item", timeout=60000)

                # Scroll to bottom to load lazy content
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(2)  # wait for lazy loading

                cards = page.query_selector_all("app-competition-listing a.item")
                if not cards:
                    print(f"⚠️ No hackathon cards found on page {page_num}")
                    continue

                for card in cards:
                    try:
                        # Name
                        name_tag = card.query_selector("h2")
                        name = name_tag.inner_text().strip() if name_tag else "No name"

                        # Link
                        link = card.get_attribute("href")
                        if not link:
                            print(f"⚠️ Skipping {name} due to missing link")
                            continue
                        link = "https://unstop.com" + link

                        # Location
                        location_tag = card.query_selector("span.ng-star-inserted")
                        location = location_tag.inner_text().strip() if location_tag else "Online"

                        # Prize
                        prize_tag = card.query_selector("div.cash_widget .title")
                        prize = prize_tag.inner_text().replace("Prizes worth", "").strip() if prize_tag else None

                        # Participants
                        participants_tag = card.query_selector("div.un_tag label")
                        participants = participants_tag.inner_text().strip() if participants_tag else None

                        # Dates (if available)
                        posted_tag = card.query_selector("div.un_tag label")
                        posted_date = None
                        if posted_tag:
                            try:
                                # example: "Posted Jan 3, 2026"
                                text = posted_tag.inner_text()
                                if "Posted" in text:
                                    date_str = text.replace("Posted", "").strip()
                                    posted_date = datetime.strptime(date_str, "%b %d, %Y").date()
                            except:
                                posted_date = None

                        # Fallback for start/end dates
                        start_date = end_date = posted_date or datetime.today().date()

                        hackathons.append({
                            "name": name,
                            "platform": "Unstop",
                            "start_date": start_date,
                            "end_date": end_date,
                            "location": location,
                            "link": link,
                            "prize": prize,
                            "participants": participants
                        })

                    except Exception as e:
                        print(f"⚠️ Failed to parse a hackathon card: {e}")
                        continue

            except Exception as e:
                print(f"❌ Failed to scrape page {page_num}: {e}")
                continue

        browser.close()

    print(f"✅ Total Unstop hackathons scraped: {len(hackathons)}")
    return hackathons
