from scrapers.devpost import fetch_devpost
from scrapers.mlh import fetch_mlh

def fetch_all_hackathons():
    data = []
    data.extend(fetch_devpost(max_pages=10))
    data.extend(fetch_mlh())
    return data
