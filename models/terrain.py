from sqlalchemy import Column, String, Float, Integer, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Mountain(Base):
    __tablename__ = "mountains"

    mountain_id = Column(String, primary_key=True)
    mountain_name = Column(String, nullable=False)
    data_version = Column(String)
    coord_system = Column(String, nullable=False, default="WGS84")
    gpx_file = Column(String)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    nodes = relationship("TrailNode", back_populates="mountain")
    links = relationship("TrailLink", back_populates="mountain")
    pois = relationship("Poi", back_populates="mountain")
    accident_history = relationship("AccidentHistory", back_populates="mountain")
    sessions = relationship("HikingSession", back_populates="mountain")


class TrailNode(Base):
    __tablename__ = "trail_nodes"

    node_id = Column(String, primary_key=True)
    mountain_id = Column(String, ForeignKey("mountains.mountain_id"), nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    altitude_m = Column(Float)
    node_type = Column(String)

    mountain = relationship("Mountain", back_populates="nodes")


class TrailLink(Base):
    __tablename__ = "trail_links"

    link_id = Column(String, primary_key=True)
    mountain_id = Column(String, ForeignKey("mountains.mountain_id"), nullable=False)
    start_node_id = Column(String, ForeignKey("trail_nodes.node_id"), nullable=False)
    end_node_id = Column(String, ForeignKey("trail_nodes.node_id"), nullable=False)
    length_m = Column(Float)
    slope_deg = Column(Float)
    course_type = Column(String)
    popular = Column(String)
    legal = Column(String)
    surface = Column(String)
    difficulty = Column(Integer)
    geometry = Column(JSON)

    mountain = relationship("Mountain", back_populates="links")


class Poi(Base):
    __tablename__ = "pois"

    poi_id = Column(Integer, primary_key=True)
    mountain_id = Column(String, ForeignKey("mountains.mountain_id"), nullable=False)
    poi_name = Column(String, nullable=False)
    cate_cd = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    altitude_m = Column(Float)
    description = Column(String)

    mountain = relationship("Mountain", back_populates="pois")
    session_events = relationship("SessionEvent", back_populates="poi")
    inference_alerts = relationship("InferenceAlert", back_populates="poi")


class AccidentHistory(Base):
    __tablename__ = "accident_history"

    accident_id = Column(Integer, primary_key=True, autoincrement=True)
    mountain_id = Column(String, ForeignKey("mountains.mountain_id"), nullable=False)
    accident_type = Column(String)
    occurrence_date = Column(DateTime)
    location_lat = Column(Float)
    location_lng = Column(Float)

    mountain = relationship("Mountain", back_populates="accident_history")
