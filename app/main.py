import asyncio
from fastapi import FastAPI
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from .database import Base, engine, SessionLocal
from .crud import upsert_hackathons
from .models import Hackathon

from .scheduler import start_scheduler
from scrapers.aggregator import fetch_all_hackathons
import httpx
from fastapi import FastAPI, Depends

from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hackathon Aggregator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- allows requests from any frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    start_scheduler()
    # Start the self-ping background task
    asyncio.create_task(self_ping())

# Self-ping task
async def self_ping():
    url = "https://hackathon-backend-3stq.onrender.com/health"
    async with httpx.AsyncClient() as client:
        while True:
            try:
                resp = await client.get(url)
                print(f"Self-ping status: {resp.status_code}")
            except Exception as e:
                print(f"Self-ping failed: {e}")
            await asyncio.sleep(5 * 60)  # 5 minutes

@app.get("/hackathons")
def fetch_hackathons(
    platform: str | None = None,
    db: Session = Depends(get_db)
):
    # Simple get all for now
    query = db.query(Hackathon)
    if platform:
        query = query.filter(Hackathon.platform == platform)
    return query.all()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/scrape-now")
def scrape_now():
    """
    Scrape hackathons and save to DB with retry logic for SSL connection issues.
    """
    # First, fetch all hackathons data
    print("🔍 Starting scrape...")
    data = fetch_all_hackathons()
    print(f"📦 Scraped {len(data)} hackathons")

    # Create a NEW session after scraping to avoid connection timeout
    db = SessionLocal()
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        try:
            added = upsert_hackathons(db, data)
            db.close()
            return {"status": "done", "added": added}
        except OperationalError as e:
            retry_count += 1
            print(f"⚠️ Database connection error (attempt {retry_count}/{max_retries}): {e}")
            db.close()
            # Create a fresh session for retry
            db = SessionLocal()
            if retry_count < max_retries:
                print("🔄 Retrying with fresh connection...")
                continue
            else:
                print("❌ Max retries reached. Connection failed.")
                return {"status": "error", "message": "Database connection failed after retries"}
        except Exception as e:
            db.close()
            print(f"❌ Unexpected error: {e}")
            return {"status": "error", "message": str(e)}

