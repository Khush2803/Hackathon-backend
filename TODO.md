# TODO: Auto-delete Expired Hackathons Implementation

## Task: Implement scheduled background job to auto-delete expired hackathons

### Steps:

1. [ ] Update `app/crud.py`

   - [ ] Add `delete_expired_hackathons()` function with database logic

2. [ ] Update `app/scheduler.py`

   - [ ] Add `cleanup_expired_hackathons()` function
   - [ ] Add scheduled job to run every 6-24 hours

3. [ ] Update `app/main.py`
   - [ ] Add POST `/cleanup-expired` manual endpoint
   - [ ] Add GET `/cleanup-status` endpoint

---

## Implementation Details:

### 1. `app/crud.py` - Add delete function:

```python
def delete_expired_hackathons(db: Session) -> int:
    """Delete hackathons where end_date < current_date"""
    from datetime import date
    now = date.today()
    expired = db.query(Hackathon).filter(Hackathon.end_date < now)
    count = expired.count()
    expired.delete(synchronize_session=False)
    db.commit()
    return count
```

### 2. `app/scheduler.py` - Add cleanup job:

```python
def cleanup_expired_hackathons():
    """Scheduled job to delete expired hackathons"""
    db = SessionLocal()
    try:
        from app.crud import delete_expired_hackathons
        count = delete_expired_hackathons(db)
        print(f"🧹 Cleaned up {count} expired hackathons")
    finally:
        db.close()

# In start_scheduler():
scheduler.add_job(cleanup_expired_hackathons, "interval", hours=12, id="cleanup_expired")
```

### 3. `app/main.py` - Add manual endpoints:

```python
@app.post("/cleanup-expired")
def cleanup_expired_manual():
    """Manually trigger cleanup of expired hackathons"""
    db = SessionLocal()
    try:
        from app.crud import delete_expired_hackathons
        count = delete_expired_hackathons(db)
        return {"status": "success", "deleted": count}
    finally:
        db.close()
```

---

## Status: Pending
