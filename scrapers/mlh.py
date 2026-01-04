import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_mlh():
    url = "https://mlh.io/seasons/2025/events"
    response = requests.get(url, timeout=30)
    soup = BeautifulSoup(response.text, "html.parser")

    hackathons = []

    events = soup.select(".event-wrapper")

    for event in events:
        try:
            name = event.select_one(".event-name").text.strip()
            link = "https://mlh.io" + event.select_one("a")["href"]
            location = event.select_one(".event-location").text.strip()

            date_text = event.select_one(".event-date").text.strip()
            start_date = end_date = datetime.today().date()  # MLH date varies

            hackathons.append({
                "name": name,
                "platform": "MLH",
                "start_date": start_date,
                "end_date": end_date,
                "location": location,
                "link": link,
                "prize": None,
                "participants": None
            })

        except Exception:
            continue

    return hackathons
