from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, JSON, ForeignKey, BigInteger, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base
import datetime

class HikingSession(Base):
    __tablename__ = "hiking_sessions"

    session_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    mountain_id = Column(String, ForeignKey("mountains.mountain_id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    start_lat = Column(Float)
    start_lng = Column(Float)
    total_distance_m = Column(Integer)
    total_ascent_m = Column(Integer)
    selected_course_id = Column(String)
    completed = Column(Boolean, default=False)
    stamp_acquired = Column(Boolean, default=False)
    source = Column(String, nullable=False)  # realtime | history
    raw_payload = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="sessions")
    mountain = relationship("Mountain", back_populates="sessions")
    biometric_batches = relationship("BiometricBatch", back_populates="session")
    emergency_triggers = relationship("EmergencyTrigger", back_populates="session")
    gps_tracks = relationship("SessionGpsTrack", back_populates="session")
    biometric_summary = relationship("SessionBiometricSummary", back_populates="session", uselist=False)
    events = relationship("SessionEvent", back_populates="session")
    feedback = relationship("SessionFeedback", back_populates="session", uselist=False)
    environment_logs = relationship("EnvironmentLog", back_populates="session")
    inference_results = relationship("InferenceResult", back_populates="session")


class BiometricBatch(Base):
    __tablename__ = "biometric_batches"
    __table_args__ = (
        UniqueConstraint("session_id", "batch_seq", name="uq_batch_idempotency"),
    )

    batch_id = Column(BigInteger, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("hiking_sessions.session_id"), nullable=False)
    batch_seq = Column(Integer)
    channel = Column(String, nullable=False)  # normal | emergency
    batch_start = Column(DateTime)
    batch_end = Column(DateTime)
    raw_payload = Column(JSON, nullable=False)
    received_at = Column(DateTime, default=datetime.datetime.utcnow)

    session = relationship("HikingSession", back_populates="biometric_batches")
    activity_samples = relationship("ActivitySample", back_populates="batch")
    heart_rate_intervals = relationship("HeartRateInterval", back_populates="batch")
    spo2_intervals = relationship("Spo2Interval", back_populates="batch")
    step_intervals = relationship("StepInterval", back_populates="batch")


class ActivitySample(Base):
    __tablename__ = "activity_samples"

    sample_id = Column(BigInteger, primary_key=True, autoincrement=True)
    batch_id = Column(BigInteger, ForeignKey("biometric_batches.batch_id"), nullable=False)
    session_id = Column(String, ForeignKey("hiking_sessions.session_id"), nullable=False)
    ts = Column(DateTime, nullable=False)
    acc_x = Column(Float, nullable=False)
    acc_y = Column(Float, nullable=False)
    acc_z = Column(Float, nullable=False)
    gps_lat = Column(Float)
    gps_lon = Column(Float)

    batch = relationship("BiometricBatch", back_populates="activity_samples")


class HeartRateInterval(Base):
    __tablename__ = "heart_rate_intervals"

    interval_id = Column(BigInteger, primary_key=True, autoincrement=True)
    batch_id = Column(BigInteger, ForeignKey("biometric_batches.batch_id"), nullable=False)
    session_id = Column(String, ForeignKey("hiking_sessions.session_id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    value_bpm = Column(Integer, nullable=False)

    batch = relationship("BiometricBatch", back_populates="heart_rate_intervals")


class Spo2Interval(Base):
    __tablename__ = "spo2_intervals"

    interval_id = Column(BigInteger, primary_key=True, autoincrement=True)
    batch_id = Column(BigInteger, ForeignKey("biometric_batches.batch_id"), nullable=False)
    session_id = Column(String, ForeignKey("hiking_sessions.session_id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    value_pct = Column(Integer, nullable=False)

    batch = relationship("BiometricBatch", back_populates="spo2_intervals")


class StepInterval(Base):
    __tablename__ = "step_intervals"

    interval_id = Column(BigInteger, primary_key=True, autoincrement=True)
    batch_id = Column(BigInteger, ForeignKey("biometric_batches.batch_id"), nullable=False)
    session_id = Column(String, ForeignKey("hiking_sessions.session_id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    value_steps = Column(Integer, nullable=False)

    batch = relationship("BiometricBatch", back_populates="step_intervals")


class EmergencyTrigger(Base):
    __tablename__ = "emergency_triggers"

    trigger_id = Column(BigInteger, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("hiking_sessions.session_id"), nullable=False)
    trigger_type = Column(String, nullable=False)  # T-1 | T-2 | T-3
    trigger_ts = Column(DateTime, nullable=False)
    trigger_value = Column(Float, nullable=False)
    gps_lat = Column(Float)
    gps_lon = Column(Float)
    raw_payload = Column(JSON, nullable=False)
    received_at = Column(DateTime, default=datetime.datetime.utcnow)

    session = relationship("HikingSession", back_populates="emergency_triggers")


class SessionGpsTrack(Base):
    __tablename__ = "session_gps_tracks"

    track_id = Column(BigInteger, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("hiking_sessions.session_id"), nullable=False)
    ts = Column(DateTime, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)

    session = relationship("HikingSession", back_populates="gps_tracks")


class SessionBiometricSummary(Base):
    __tablename__ = "session_biometric_summary"

    summary_id = Column(BigInteger, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("hiking_sessions.session_id"), nullable=False, unique=True)
    hr_mean = Column(Integer, nullable=False)
    hr_max = Column(Integer, nullable=False)
    hr_rest = Column(Integer)
    spo2_mean = Column(Integer)
    steps_total = Column(Integer, nullable=False)

    session = relationship("HikingSession", back_populates="biometric_summary")


class SessionEvent(Base):
    __tablename__ = "session_events"

    event_id = Column(BigInteger, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("hiking_sessions.session_id"), nullable=False)
    ts = Column(DateTime, nullable=False)
    event_type = Column(String, nullable=False)  # rest | water | emergency | detour | descent
    poi_id = Column(Integer, ForeignKey("pois.poi_id"))
    duration_min = Column(Integer)

    session = relationship("HikingSession", back_populates="events")
    poi = relationship("Poi", back_populates="session_events")


class SessionFeedback(Base):
    __tablename__ = "session_feedback"

    feedback_id = Column(BigInteger, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("hiking_sessions.session_id"), nullable=False, unique=True)
    difficulty_rating = Column(Integer)
    satisfaction = Column(Integer)
    fatigue_level = Column(Integer)

    session = relationship("HikingSession", back_populates="feedback")


class EnvironmentLog(Base):
    __tablename__ = "environment_logs"

    env_id = Column(BigInteger, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("hiking_sessions.session_id"), nullable=False)
    recorded_at = Column(DateTime, nullable=False)
    temperature = Column(Float)
    humidity = Column(Float)
    cellular_signal = Column(Integer)
    precipitation_mm = Column(Float)
    lightning_detected = Column(Boolean, default=False)

    session = relationship("HikingSession", back_populates="environment_logs")


class InferenceResult(Base):
    __tablename__ = "inference_results"

    result_id = Column(BigInteger, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("hiking_sessions.session_id"), nullable=False)
    uuid = Column(String, nullable=False)
    ts = Column(DateTime, nullable=False)
    user_lat = Column(Float)
    user_lon = Column(Float)
    e1_biometric = Column(Float)
    e2_combined = Column(Float)
    risk_representative = Column(Float)
    fatigue_state = Column(String)
    fatigue_confidence = Column(Float)
    nearest_shelter = Column(JSON)
    descent_required = Column(Boolean, default=False)
    descent_reason = Column(String)
    remaining_daylight_min = Column(Integer)
    course_recommendation = Column(JSON)
    raw_payload = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    session = relationship("HikingSession", back_populates="inference_results")
    alerts = relationship("InferenceAlert", back_populates="result")


class InferenceAlert(Base):
    __tablename__ = "inference_alerts"

    alert_id = Column(BigInteger, primary_key=True, autoincrement=True)
    result_id = Column(BigInteger, ForeignKey("inference_results.result_id"), nullable=False)
    session_id = Column(String, ForeignKey("hiking_sessions.session_id"), nullable=False)
    alert_type = Column(String, nullable=False)
    alert_level = Column(Integer, nullable=False)
    title = Column(String)
    message = Column(String)
    location_lat = Column(Float)
    location_lon = Column(Float)
    location_poi_id = Column(Integer, ForeignKey("pois.poi_id"))
    detour_available = Column(Boolean)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    result = relationship("InferenceResult", back_populates="alerts")
    poi = relationship("Poi", back_populates="inference_alerts")
