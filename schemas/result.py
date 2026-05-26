# DTO-5 스키마 코드

from pydantic import BaseModel
from typing import List, Optional

class Location(BaseModel):
    lat: float
    lon: float

class Course(BaseModel):
    course_id: str
    name: str
    score: float
    distance_m: int
    est_min: int
    difficulty: int

class CourseRecommendation(BaseModel):
    top3_courses: List[Course]

class Risk(BaseModel):
    e1_biometric: float
    e2_combined: float
    representative: float

class NearestShelter(BaseModel):
    poi_id: int
    name: str
    lat: float
    lon: float
    distance_m: int
    est_min: int

class Fatigue(BaseModel):
    state: str
    confidence: float
    nearest_shelter: Optional[NearestShelter] = None

class DescentWarning(BaseModel):
    required: bool
    reason: Optional[str] = None
    remaining_daylight_min: Optional[int] = None

class Alert(BaseModel):
    type: str
    level: int
    title: str
    message: str
    subtype: Optional[str] = None
    location: Optional[Location] = None
    detour_available: Optional[bool] = None

class InferenceResult(BaseModel):
    type: str
    uuid: str
    userId: str
    timestamp: str
    user_location: Location
    course_recommendation: Optional[CourseRecommendation] = None
    risk: Optional[Risk] = None
    fatigue: Optional[Fatigue] = None
    descent_warning: Optional[DescentWarning] = None
    alerts: Optional[List[Alert]] = None