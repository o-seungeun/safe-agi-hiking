from fastapi import APIRouter, Header, Depends
from sqlalchemy.orm import Session
from schemas.history import HikingHistory
from schemas.common import CommonResponse
from models.users import User
from models.sessions import (
    HikingSession, SessionGpsTrack,
    SessionBiometricSummary, SessionEvent, SessionFeedback
)
from database import get_db
from utils import success_response, COMMON_RESPONSES
import datetime

router = APIRouter()

@router.post("/history",
    response_model=CommonResponse,
    summary="등반 이력 데이터 수신",
    description="사용자 과거 등반 세션 이력 데이터 수신. 초기 대량 전송 후 월 1회 또는 일정 세션 누적 시 갱신.",
    responses=COMMON_RESPONSES
)
async def receive_history(data: HikingHistory, userId: str = Header(...), db: Session = Depends(get_db)):
    p = data.user_profile

    # User upsert
    user = db.get(User, p.userId)
    if not user:
        db.add(User(
            user_id=p.userId,
            age_group=p.age_group,
            gender=p.gender,
            hiking_experience_years=p.hiking_experience_years,
            fitness_level=p.fitness_level,
            chronic_conditions=p.chronic_conditions,
            total_sessions=p.total_sessions,
            preferred_difficulty=p.preferred_difficulty
        ))
    else:
        user.age_group = p.age_group
        user.fitness_level = p.fitness_level
        user.total_sessions = p.total_sessions
        user.preferred_difficulty = p.preferred_difficulty
    db.flush()

    for s in data.sessions:
        # HikingSession upsert
        session = db.get(HikingSession, s.session_id)
        if not session:
            db.add(HikingSession(
                session_id=s.session_id,
                user_id=p.userId,
                mountain_id=s.mountain_id,
                start_time=datetime.datetime.fromisoformat(s.start_time.replace("Z", "+00:00")),
                end_time=datetime.datetime.fromisoformat(s.end_time.replace("Z", "+00:00")),
                total_distance_m=s.total_distance_m,
                total_ascent_m=s.total_ascent_m,
                selected_course_id=s.selected_course_id,
                completed=s.completed,
                stamp_acquired=s.stamp_acquired,
                source="history"
            ))
            db.flush()

            # GPS Track
            for g in s.gps_track:
                db.add(SessionGpsTrack(
                    session_id=s.session_id,
                    ts=datetime.datetime.fromisoformat(g.timestamp.replace("Z", "+00:00")),
                    lat=g.lat,
                    lon=g.lon
                ))

            # Biometric Summary
            b = s.biometric_summary
            db.add(SessionBiometricSummary(
                session_id=s.session_id,
                hr_mean=b.hr_mean,
                hr_max=b.hr_max,
                hr_rest=b.hr_rest,
                spo2_mean=b.spo2_mean,
                steps_total=b.steps_total
            ))

            # Events
            for e in s.events:
                db.add(SessionEvent(
                    session_id=s.session_id,
                    ts=datetime.datetime.fromisoformat(e.timestamp.replace("Z", "+00:00")),
                    event_type=e.event_type,
                    poi_id=e.poi_id,
                    duration_min=e.duration_min
                ))

            # Feedback
            f = s.user_feedback
            db.add(SessionFeedback(
                session_id=s.session_id,
                difficulty_rating=f.difficulty_rating,
                satisfaction=f.satisfaction,
                fatigue_level=f.fatigue_level
            ))

    db.commit()
    return success_response()
