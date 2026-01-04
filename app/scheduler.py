# app/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from scrapers.aggregator import fetch_all_hackathons
from app.database import SessionLocal
from app.crud import upsert_hackathons

def scrape_and_update_db():
    print("🔄 Running scheduled scrape...")
    db = SessionLocal()
    try:
        hackathons = fetch_all_hackathons()
        added = upsert_hackathons(db, hackathons)
        print(f"✅ Scheduled scrape done. {added} new hackathons added.")
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Run every 24 hours
    scheduler.add_job(scrape_and_update_db, "interval", hours=24, id="daily_scrape")
    scheduler.start()
    print("⏰ Scheduler started, scraping every 24 hours.")
