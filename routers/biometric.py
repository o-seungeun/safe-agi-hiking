from fastapi import APIRouter, Header, Depends
from sqlalchemy.orm import Session
from schemas.biometric import BiometricNormal, BiometricEmergency
from schemas.common import CommonResponse
from models.biometric import BiometricSession, Sample, HeartRate, BloodOxygen, Step
from database import get_db
from services.result import send_result
from utils import success_response, error_response, COMMON_RESPONSES

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

    existing = db.get(BiometricSession, data.uuid)
    if not existing:
        session = BiometricSession(uuid=data.uuid, user_id=userId)
        db.add(session)

    for s in data.samples:
        sample = Sample(uuid=data.uuid, ts=s.ts, acc_x=s.acc_x, acc_y=s.acc_y, acc_z=s.acc_z, lat=s.gps.lat, lon=s.gps.lon)
        db.add(sample)

    for hr in data.heart_rates:
        heart_rate = HeartRate(uuid=data.uuid, start_time=hr.start_time, end_time=hr.end_time, value=hr.value)
        db.add(heart_rate)

    for bo in data.blood_oxygens:
        blood_oxygen = BloodOxygen(uuid=data.uuid, start_time=bo.start_time, end_time=bo.end_time, value=bo.value)
        db.add(blood_oxygen)

    for st in data.steps:
        step = Step(uuid=data.uuid, start_time=st.start_time, end_time=st.end_time, value=st.value)
        db.add(step)

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

    existing = db.get(BiometricSession, data.uuid)
    if not existing:
        return error_response(
            code="101",
            msg="uuid가 등록되지 않은 세션. uuid 재생성 후 재전송 필요."
        )

    for s in data.samples:
        sample = Sample(uuid=data.uuid, ts=s.ts, acc_x=s.acc_x, acc_y=s.acc_y, acc_z=s.acc_z, lat=s.gps.lat, lon=s.gps.lon)
        db.add(sample)

    for hr in data.heart_rates:
        heart_rate = HeartRate(uuid=data.uuid, start_time=hr.start_time, end_time=hr.end_time, value=hr.value)
        db.add(heart_rate)

    for bo in data.blood_oxygens:
        blood_oxygen = BloodOxygen(uuid=data.uuid, start_time=bo.start_time, end_time=bo.end_time, value=bo.value)
        db.add(blood_oxygen)

    for st in data.steps:
        step = Step(uuid=data.uuid, start_time=st.start_time, end_time=st.end_time, value=st.value)
        db.add(step)

    db.commit()

    await send_result(
        uuid=data.uuid,
        user_id=userId,
        lat=data.gps_at_trigger.lat,
        lon=data.gps_at_trigger.lon
    )

    return success_response()