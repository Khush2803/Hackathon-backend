from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

BASE_URLS = [
    "https://devpost.com/hackathons",
    "https://devpost.com/hackathons?search=ai",
    "https://devpost.com/hackathons?search=blockchain",
    "https://devpost.com/hackathons?search=machine+learning",
]

def fetch_hackathons():
    hackathons = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0",
            viewport={"width": 1400, "height": 900}
        )
        page = context.new_page()

        for url in BASE_URLS:
            print(f"\n🔍 Scraping Devpost: {url}")

            page.goto(url, wait_until="networkidle", timeout=60000)

            # Accept cookies if present
            try:
                page.locator("button:has-text('Accept')").first.click(timeout=3000)
            except:
                pass

            prev_count = 0

            # Infinite scroll
            for _ in range(10):
                page.mouse.wheel(0, 4000)
                time.sleep(2)

                soup = BeautifulSoup(page.content(), "html.parser")
                cards = soup.select("a[href*='.devpost.com']")

                if len(cards) == prev_count:
                    break
                prev_count = len(cards)

            soup = BeautifulSoup(page.content(), "html.parser")

            # REAL selector
            cards = soup.select("a[href*='.devpost.com']:has(h3)")

            print(f"➡️ Found {len(cards)} cards")

            for card in cards:
                name_el = card.select_one("h3")
                if not name_el:
                    continue

                link = card.get("href")
                if not link.startswith("http"):
                    link = "https://devpost.com" + link

                if link in hackathons:
                    continue

                # Try to extract image URL from the card
                image_url = None
                img_el = card.select_one("img")
                if img_el:
                    image_url = img_el.get("src") or img_el.get("data-src") or img_el.get("data-srcset")
                    if image_url and not image_url.startswith("http"):
                        image_url = "https://devpost.com" + image_url

                hackathons[link] = {
                    "name": name_el.text.strip(),
                    "platform": "Devpost",
                    "link": link,
                    "location": "Online",
                    "image_url": image_url,
                }

                print(
                    f"Name: {name_el.text.strip()}\n"
                    f"Platform: Devpost\n"
                    f"Location: Online\n"
                    f"Image: {image_url}\n"
                    f"Link: {link}\n"
                    f"{'-'*40}"
                )

        browser.close()

    print(f"\n✅ Devpost unique hackathons scraped: {len(hackathons)}")
    return list(hackathons.values())


if __name__ == "__main__":
    fetch_hackathons()

