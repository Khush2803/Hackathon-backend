from sqlalchemy import Column, Integer, String, Date
from .database import Base

class Hackathon(Base):
    __tablename__ = "hackathons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    location = Column(String, nullable=False)
    link = Column(String, nullable=False, unique=True)
    prize = Column(String)
    participants = Column(String)
