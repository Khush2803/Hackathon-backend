from playwright.sync_api import sync_playwright
import time

HACKEREARTH_URL = "https://www.hackerearth.com/challenges/"

def fetch_hackerearth_hackathons():
    hackathons = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(HACKEREARTH_URL, timeout=60000)

        # Wait for the challenge cards to load
        page.wait_for_selector("div.challenge-card", timeout=15000)
        time.sleep(2)

        # Scroll to load more
        previous_count = 0
        idle_scrolls = 0
        while idle_scrolls < 3:
            page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            time.sleep(2)
            cards = page.locator("div.challenge-card")
            count = cards.count()
            if count == previous_count:
                idle_scrolls += 1
            else:
                idle_scrolls = 0
            previous_count = count

        cards = page.locator("div.challenge-card")
        total = cards.count()
        for i in range(total):
            try:
                title_el = cards.nth(i).locator("h3").first
                title = title_el.inner_text().strip() if title_el.count() > 0 else ""

                link_el = cards.nth(i).locator("a[href]").first
                link = link_el.get_attribute("href") if link_el.count() > 0 else ""
                if link and not link.startswith("http"):
                    link = "https://hackerearth.com" + link

                # Try to extract image URL from the card
                image_url = None
                try:
                    img_el = cards.nth(i).locator("img").first
                    if img_el.count() > 0:
                        image_url = img_el.get_attribute("src") or img_el.get_attribute("data-src")
                        if image_url and not image_url.startswith("http"):
                            image_url = "https:" + image_url
                except Exception:
                    pass

                hackathons[link] = {
                    "name": title,
                    "platform": "HackerEarth",
                    "location": "Online",
                    "link": link,
                    "image_url": image_url,
                }

                print(
                    f"Name: {title}\nPlatform: HackerEarth\nLocation: Online\nImage: {image_url}\nLink: {link}\n{'-'*40}"
                )

            except Exception as e:
                print(f"⚠️ Failed to parse card {i}: {e}")

        browser.close()

    print(f"\n✅ TOTAL HackerEarth hackathons scraped: {len(hackathons)}")
    return list(hackathons.values())


if __name__ == "__main__":
    fetch_hackerearth_hackathons()

