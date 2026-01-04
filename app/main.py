from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from .crud import get_hackathons, upsert_hackathons
from .scheduler import start_scheduler
from scrapers.aggregator import fetch_all_hackathons

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hackathon Aggregator API")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    start_scheduler()

@app.get("/hackathons")
def fetch_hackathons(
    platform: str | None = Query(None),
    db: Session = Depends(get_db)
):
    return get_hackathons(db, platform=platform)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/scrape-now")
def scrape_now(db: Session = Depends(get_db)):
    data = fetch_all_hackathons()
    added = upsert_hackathons(db, data)
    return {"status": "done", "added": added}
