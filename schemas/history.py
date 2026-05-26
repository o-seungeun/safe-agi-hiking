# DTO-4 스키마 코드

from pydantic import BaseModel
from typing import List, Optional

class UserProfile(BaseModel):
    userId: str
    age_group: str
    gender: str
    hiking_experience_years: int
    fitness_level: int
    chronic_conditions: List[str]
    total_sessions: int
    preferred_difficulty: Optional[int] = None

class GPSTrack(BaseModel):
    timestamp: str
    lat: float
    lon: float

class BiometricSummary(BaseModel):
    hr_mean: int
    hr_max: int
    hr_rest: Optional[int] = None
    spo2_mean: Optional[int] = None
    steps_total: int

class Event(BaseModel):
    timestamp: str
    event_type: str
    poi_id: Optional[int] = None
    duration_min: Optional[int] = None

class UserFeedback(BaseModel):
    difficulty_rating: Optional[int] = None
    satisfaction: Optional[int] = None
    fatigue_level: Optional[int] = None

class Session(BaseModel):
    session_id: str
    mountain_id: str
    mountain_name: str
    start_time: str
    end_time: str
    total_distance_m: int
    total_ascent_m: Optional[int] = None
    selected_course_id: Optional[str] = None
    completed: bool
    stamp_acquired: bool
    gps_track: List[GPSTrack]
    biometric_summary: BiometricSummary
    events: List[Event]
    user_feedback: UserFeedback

class HikingHistory(BaseModel):
    data_type: str
    schema_ver: str
    export_date: str
    privacy_note: Optional[str] = None
    user_profile: UserProfile
    sessions: List[Session]