from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .models import Hackathon

def get_hackathons(db: Session, platform: str | None = None, skip: int = 0, limit: int = 100):
    """
    Retrieves hackathons from the database with optional platform filtering and pagination.
    """
    query = db.query(Hackathon)
    if platform:
        query = query.filter(Hackathon.platform == platform)
    return query.offset(skip).limit(limit).all()

def upsert_hackathons(db: Session, hackathons: list):
    """
    Inserts new hackathons and skips duplicates based on the 'link' field.
    Returns the number of new hackathons added.
    """
    added_count = 0

    for h in hackathons:
        if not h.get("link"):
            continue

        # Check if this hackathon already exists
        exists = db.query(Hackathon).filter(Hackathon.link == h["link"]).first()
        if exists:
            continue  # Skip duplicates

        # Create new hackathon
        hack = Hackathon(
            name=h.get("name", ""),
            platform=h.get("platform", ""),
            start_date=h.get("start_date"),
            end_date=h.get("end_date"),
            location=h.get("location", ""),
            link=h.get("link", ""),
            prize=h.get("prize"),
            participants=h.get("participants"),
        )

        db.add(hack)
        added_count += 1

    try:
        db.commit()
    except IntegrityError:
        db.rollback()  # Safety in case something slipped through
        print("⚠️ Duplicate detected, skipping conflicting entries")

    return added_count
