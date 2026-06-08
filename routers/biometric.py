from fastapi import APIRouter, Header, Depends
from sqlalchemy.orm import Session
from schemas.biometric import BiometricNormal, BiometricEmergency
from schemas.common import CommonResponse
from models.sessions import (
    HikingSession, BiometricBatch,
    ActivitySample, HeartRateInterval, Spo2Interval, StepInterval,
    EmergencyTrigger
)
from database import get_db
from services.result import send_result
from utils import success_response, error_response, COMMON_RESPONSES
import datetime

router = APIRouter()

@router.post("/biometric/normal",
    response_model=CommonResponse,
    summary="일반 채널 생체 데이터 수신",
    description="웨어러블(워치)에서 1분간 수집된 60개의 samples를 포함한 생체 데이터 수신.",
    responses={
        400: {"description": "samples 60개 미충족", "content": {"application/json": {"example": {
            "code": "100",
            "msg": "samples 배열 크기가 60이어야 함. 수신 크기: N"
        }}}},
        **COMMON_RESPONSES
    }
)
async def receive_normal(data: BiometricNormal, userId: str = Header(...), db: Session = Depends(get_db)):
    if len(data.samples) != 60:
        return error_response(
            code="100",
            msg=f"samples 배열 크기가 60이어야 함. 수신 크기: {len(data.samples)}"
        )

    # 세션 없으면 생성
    existing = db.get(HikingSession, data.uuid)
    if not existing:
        session = HikingSession(
            session_id=data.uuid,
            user_id=userId,
            start_time=datetime.datetime.utcnow(),
            source="realtime"
        )
        db.add(session)
        db.flush()

    # 배치 생성
    batch_start = datetime.datetime.fromisoformat(data.samples[0].ts.replace("Z", "+00:00"))
    batch_end = datetime.datetime.fromisoformat(data.samples[-1].ts.replace("Z", "+00:00"))
    batch = BiometricBatch(
        session_id=data.uuid,
        channel="normal",
        batch_start=batch_start,
        batch_end=batch_end,
        raw_payload=data.model_dump()
    )
    db.add(batch)
    db.flush()

    # activity_samples 저장
    for s in data.samples:
        sample = ActivitySample(
            batch_id=batch.batch_id,
            session_id=data.uuid,
            ts=datetime.datetime.fromisoformat(s.ts.replace("Z", "+00:00")),
            acc_x=s.acc_x,
            acc_y=s.acc_y,
            acc_z=s.acc_z,
            gps_lat=s.gps.lat,
            gps_lon=s.gps.lon
        )
        db.add(sample)

    # heart_rate_intervals 저장
    for hr in data.heart_rates:
        db.add(HeartRateInterval(
            batch_id=batch.batch_id,
            session_id=data.uuid,
            start_time=datetime.datetime.fromisoformat(hr.start_time.replace("Z", "+00:00")),
            end_time=datetime.datetime.fromisoformat(hr.end_time.replace("Z", "+00:00")),
            value_bpm=hr.value
        ))

    # spo2_intervals 저장
    for bo in data.blood_oxygens:
        db.add(Spo2Interval(
            batch_id=batch.batch_id,
            session_id=data.uuid,
            start_time=datetime.datetime.fromisoformat(bo.start_time.replace("Z", "+00:00")),
            end_time=datetime.datetime.fromisoformat(bo.end_time.replace("Z", "+00:00")),
            value_pct=bo.value
        ))

    # step_intervals 저장
    for st in data.steps:
        db.add(StepInterval(
            batch_id=batch.batch_id,
            session_id=data.uuid,
            start_time=datetime.datetime.fromisoformat(st.start_time.replace("Z", "+00:00")),
            end_time=datetime.datetime.fromisoformat(st.end_time.replace("Z", "+00:00")),
            value_steps=st.value
        ))

    db.commit()

    last_sample = data.samples[-1]
    await send_result(
        uuid=data.uuid,
        user_id=userId,
        lat=last_sample.gps.lat,
        lon=last_sample.gps.lon
    )

    return success_response()


@router.post("/biometric/emergency",
    response_model=CommonResponse,
    summary="긴급 채널 생체 데이터 수신",
    description="낙상(T1), 심박 급변(T2), 장시간 정지(T3) 감지 시 즉시 전송되는 긴급 데이터 수신.",
    responses={
        400: {"description": "세션 미등록 또는 samples 10개 초과", "content": {"application/json": {"example": {
            "code": "100",
            "msg": "uuid가 등록되지 않은 세션. uuid 재생성 후 재전송 필요."
        }}}},
        **COMMON_RESPONSES
    }
)
async def receive_emergency(data: BiometricEmergency, userId: str = Header(...), db: Session = Depends(get_db)):
    if len(data.samples) > 10:
        return error_response(
            code="100",
            msg=f"긴급 채널 samples 배열 크기는 최대 10개. 수신 크기: {len(data.samples)}"
        )

    existing = db.get(HikingSession, data.uuid)
    if not existing:
        return error_response(
            code="101",
            msg="uuid가 등록되지 않은 세션. uuid 재생성 후 재전송 필요."
        )

    # 긴급 트리거 저장
    trigger = EmergencyTrigger(
        session_id=data.uuid,
        trigger_type=data.trigger_type,
        trigger_ts=datetime.datetime.fromisoformat(data.trigger_ts.replace("Z", "+00:00")),
        trigger_value=data.trigger_value,
        gps_lat=data.gps_at_trigger.lat,
        gps_lon=data.gps_at_trigger.lon,
        raw_payload=data.model_dump()
    )
    db.add(trigger)
    db.flush()

    # 긴급 배치 저장
    batch = BiometricBatch(
        session_id=data.uuid,
        channel="emergency",
        raw_payload=data.model_dump()
    )
    db.add(batch)
    db.flush()

    # activity_samples 저장
    for s in data.samples:
        db.add(ActivitySample(
            batch_id=batch.batch_id,
            session_id=data.uuid,
            ts=datetime.datetime.fromisoformat(s.ts.replace("Z", "+00:00")),
            acc_x=s.acc_x,
            acc_y=s.acc_y,
            acc_z=s.acc_z,
            gps_lat=s.gps.lat,
            gps_lon=s.gps.lon
        ))

    # heart_rate_intervals 저장
    for hr in data.heart_rates:
        db.add(HeartRateInterval(
            batch_id=batch.batch_id,
            session_id=data.uuid,
            start_time=datetime.datetime.fromisoformat(hr.start_time.replace("Z", "+00:00")),
            end_time=datetime.datetime.fromisoformat(hr.end_time.replace("Z", "+00:00")),
            value_bpm=hr.value
        ))

    # spo2_intervals 저장
    for bo in data.blood_oxygens:
        db.add(Spo2Interval(
            batch_id=batch.batch_id,
            session_id=data.uuid,
            start_time=datetime.datetime.fromisoformat(bo.start_time.replace("Z", "+00:00")),
            end_time=datetime.datetime.fromisoformat(bo.end_time.replace("Z", "+00:00")),
            value_pct=bo.value
        ))

    # step_intervals 저장
    for st in data.steps:
        db.add(StepInterval(
            batch_id=batch.batch_id,
            session_id=data.uuid,
            start_time=datetime.datetime.fromisoformat(st.start_time.replace("Z", "+00:00")),
            end_time=datetime.datetime.fromisoformat(st.end_time.replace("Z", "+00:00")),
            value_steps=st.value
        ))

    db.commit()

    await send_result(
        uuid=data.uuid,
        user_id=userId,
        lat=data.gps_at_trigger.lat,
        lon=data.gps_at_trigger.lon
    )

    return success_response()
