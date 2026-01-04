from .devpost import fetch_hackathons as fetch_devpost_hackathons
from .unstop import fetch_unstop_hackathons

def fetch_all_hackathons(max_pages_devpost=10, max_pages_unstop=5):
    all_hackathons = []

    print("🌐 Fetching hackathons from Devpost...")
    try:
        devpost_hacks = fetch_devpost_hackathons(max_pages=max_pages_devpost)
        all_hackathons.extend(devpost_hacks)
        print(f"✅ Devpost: {len(devpost_hacks)} hackathons fetched")
    except Exception as e:
        print(f"❌ Devpost fetch failed: {e}")

    print("🌐 Fetching hackathons from Unstop...")
    try:
        unstop_hacks = fetch_unstop_hackathons(max_pages=max_pages_unstop)
        all_hackathons.extend(unstop_hacks)
        print(f"✅ Unstop: {len(unstop_hacks)} hackathons fetched")
    except Exception as e:
        print(f"❌ Unstop fetch failed: {e}")

    print(f"🌟 Total hackathons fetched: {len(all_hackathons)}")
    return all_hackathons
