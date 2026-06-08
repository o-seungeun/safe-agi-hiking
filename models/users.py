from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True)
    age_group = Column(String)
    gender = Column(String)
    hiking_experience_years = Column(Integer, nullable=False, default=0)
    fitness_level = Column(Integer, nullable=False)
    chronic_conditions = Column(JSON, nullable=False, default=list)
    total_sessions = Column(Integer, nullable=False, default=0)
    preferred_difficulty = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    sessions = relationship("HikingSession", back_populates="user")
