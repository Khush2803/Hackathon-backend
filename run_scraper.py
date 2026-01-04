from app.database import SessionLocal
from scrapers.aggregator import fetch_all_hackathons
from app.crud import upsert_hackathons

def run_once():
    print("🚀 Starting one-time hackathon scraping...")
    db = SessionLocal()
    data = fetch_all_hackathons()
    added = upsert_hackathons(db, data)
    db.close()
    print(f"✅ Done. Added {added} new hackathons.")

if __name__ == "__main__":
    run_once()
