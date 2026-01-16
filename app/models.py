from sqlalchemy import Column, Integer, String, Date, DateTime
from .database import Base
from datetime import datetime

class Hackathon(Base):
    __tablename__ = "hackathons"

    id = Column(Integer, primary_key=True, index=True)

    # 🔑 Stable unique identity (platform + source id / link hash)
    external_id = Column(String, unique=True, index=True, nullable=False)

    name = Column(String, nullable=False)
    platform = Column(String, nullable=False)

    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    location = Column(String, nullable=True)

    # ❗ NOT unique anymore
    link = Column(String, nullable=True)

    prize = Column(String, nullable=True)
    participants = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    image_url = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
