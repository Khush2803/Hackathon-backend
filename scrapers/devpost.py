from playwright.sync_api import sync_playwright
from datetime import datetime

def fetch_hackathons(max_pages=10):
    hackathons = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for page_num in range(1, max_pages + 1):
            url = f"https://devpost.com/hackathons?page={page_num}"
            print(f"Scraping Devpost page {page_num}")

            page.goto(url, timeout=60000)
            page.wait_for_selector("div.hackathon-tile", timeout=30000)

            cards = page.query_selector_all("div.hackathon-tile")

            for card in cards:
                try:
                    name = card.query_selector("h3.mb-4").inner_text().strip()

                    link = card.query_selector(
                        "a.flex-row.tile-anchor"
                    ).get_attribute("href")

                    prize_div = card.query_selector("div.prize span.prize-amount")
                    prize = prize_div.inner_text().strip() if prize_div else None

                    participants_div = card.query_selector("div.participants strong")
                    participants = (
                        participants_div.inner_text().strip()
                        if participants_div else None
                    )

                    dates_div = card.query_selector("div.submission-period")
                    try:
                        start_str, end_str = dates_div.inner_text().strip().split(" - ")
                        start_date = datetime.strptime(start_str, "%b %d, %Y").date()
                        end_date = datetime.strptime(end_str, "%b %d, %Y").date()
                    except:
                        start_date = end_date = datetime.today().date()

                    location_div = card.query_selector("div.info span")
                    location = (
                        location_div.inner_text().strip()
                        if location_div else "Online"
                    )

                    hackathons.append({
                        "name": name,
                        "platform": "Devpost",
                        "start_date": start_date,
                        "end_date": end_date,
                        "location": location,
                        "link": link,
                        "prize": prize,
                        "participants": participants
                    })

                except Exception:
                    continue

        browser.close()

    return hackathons
