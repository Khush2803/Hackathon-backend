from playwright.sync_api import sync_playwright
import time

MLH_URL = "https://mlh.io/seasons/2026/events"

def fetch_mlh_hackathons():
    hackathons = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(MLH_URL, timeout=60000)
        page.wait_for_timeout(4000)

        cards = page.locator("div.event-card")
        count = cards.count()

        for i in range(count):
            try:
                title = cards.nth(i).locator("h3").inner_text().strip()
                link_el = cards.nth(i).locator("a[href]")
                link = link_el.get_attribute("href")
                if not link.startswith("http"):
                    link = "https://mlh.io" + link

                location = cards.nth(i).locator(".event-location").inner_text().strip()
                date = cards.nth(i).locator(".event-date").inner_text().strip()

                # Try to extract image URL from the card
                image_url = None
                try:
                    # Try to find an image tag with logo/banner
                    img_el = cards.nth(i).locator("img")
                    if img_el.count() > 0:
                        image_url = img_el.get_attribute("src")
                        if image_url and not image_url.startswith("http"):
                            image_url = "https:" + image_url
                except Exception:
                    pass

                hackathons[link] = {
                    "name": title,
                    "platform": "MLH",
                    "location": location,
                    "date": date,
                    "link": link,
                    "image_url": image_url,
                }

                print(
                    f"Name: {title}\nPlatform: MLH\nLocation: {location}\nDate: {date}\nImage: {image_url}\nLink: {link}\n{'-'*40}"
                )

            except Exception as e:
                print(f"⚠️ Failed to parse card {i}: {e}")

        browser.close()

    print(f"\n✅ TOTAL MLH hackathons scraped: {len(hackathons)}")
    return list(hackathons.values())


if __name__ == "__main__":
    fetch_mlh_hackathons()

