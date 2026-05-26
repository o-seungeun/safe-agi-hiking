from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class BiometricSession(Base):
    __tablename__ = "biometric_sessions"
    
    uuid = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    samples = relationship("Sample", back_populates="session")
    heart_rates = relationship("HeartRate", back_populates="session")
    blood_oxygens = relationship("BloodOxygen", back_populates="session")
    steps = relationship("Step", back_populates="session")

class Sample(Base):
    __tablename__ = "samples"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String, ForeignKey("biometric_sessions.uuid"))
    ts = Column(String)
    acc_x = Column(Float)
    acc_y = Column(Float)
    acc_z = Column(Float)
    lat = Column(Float)
    lon = Column(Float)
    
    session = relationship("BiometricSession", back_populates="samples")

class HeartRate(Base):
    __tablename__ = "heart_rates"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String, ForeignKey("biometric_sessions.uuid"))
    start_time = Column(String)
    end_time = Column(String)
    value = Column(Integer)
    
    session = relationship("BiometricSession", back_populates="heart_rates")

class BloodOxygen(Base):
    __tablename__ = "blood_oxygens"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String, ForeignKey("biometric_sessions.uuid"))
    start_time = Column(String)
    end_time = Column(String)
    value = Column(Integer)
    
    session = relationship("BiometricSession", back_populates="blood_oxygens")

class Step(Base):
    __tablename__ = "steps"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String, ForeignKey("biometric_sessions.uuid"))
    start_time = Column(String)
    end_time = Column(String)
    value = Column(Integer)
    
    session = relationship("BiometricSession", back_populates="steps")