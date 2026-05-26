from fastapi import APIRouter, Header, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from schemas.biometric import BiometricNormal, BiometricEmergency
from models.biometric import BiometricSession, Sample, HeartRate, BloodOxygen, Step
from database import get_db
from services.result import send_result
from datetime import datetime

router = APIRouter()

@router.post("/biometric/normal",
    summary="일반 채널 생체 데이터 수신",
    description="웨어러블(워치)에서 1분간 수집된 60개의 samples를 포함한 생체 데이터 수신.",
    responses={
        400: {"description": "잘못된 요청", "content": {"application/json": {"example": {
            "type": "error",
            "uuid": "string",
            "code": "INVALID_BATCH_SIZE",
            "message": "samples 배열 크기가 60이어야 함. 수신 크기: N",
            "timestamp": "2026-05-26T00:00:00Z"
        }}}}
    }
)
async def receive_normal(data: BiometricNormal, userId: str = Header(...), db: Session = Depends(get_db)):
    # samples 60개 검증
    if len(data.samples) != 60:
        return JSONResponse(status_code=400, content={
            "type": "error",
            "uuid": data.uuid,
            "code": "INVALID_BATCH_SIZE",
            "message": f"samples 배열 크기가 60이어야 함. 수신 크기: {len(data.samples)}",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })

    # 세션 존재 여부 확인
    existing = db.get(BiometricSession, data.uuid)
    if not existing:
        session = BiometricSession(uuid=data.uuid, user_id=userId)
        db.add(session)
    
    # 샘플 저장
    for s in data.samples:
        sample = Sample(uuid=data.uuid, ts=s.ts, acc_x=s.acc_x, acc_y=s.acc_y, acc_z=s.acc_z, lat=s.gps.lat, lon=s.gps.lon)
        db.add(sample)
    
    # 심박수 저장
    for hr in data.heart_rates:
        heart_rate = HeartRate(uuid=data.uuid, start_time=hr.start_time, end_time=hr.end_time, value=hr.value)
        db.add(heart_rate)
    
    # 혈중산소 저장
    for bo in data.blood_oxygens:
        blood_oxygen = BloodOxygen(uuid=data.uuid, start_time=bo.start_time, end_time=bo.end_time, value=bo.value)
        db.add(blood_oxygen)
    
    # 걸음수 저장
    for st in data.steps:
        step = Step(uuid=data.uuid, start_time=st.start_time, end_time=st.end_time, value=st.value)
        db.add(step)
    
    db.commit()

    # 마지막 샘플 GPS 위치 추출 후 아이나비로 결과 전송
    last_sample = data.samples[-1]
    await send_result_to_airnavi(
        uuid=data.uuid,
        user_id=userId,
        lat=last_sample.gps.lat,
        lon=last_sample.gps.lon
    )

    return {"status": "ok", "uuid": data.uuid, "userId": userId}


@router.post("/biometric/emergency",
    summary="긴급 채널 생체 데이터 수신",
    description="낙상(T1), 심박 급변(T2), 장시간 정지(T3) 감지 시 즉시 전송되는 긴급 데이터 수신.",
    responses={
        400: {"description": "잘못된 요청", "content": {"application/json": {"example": {
            "type": "error",
            "uuid": "string",
            "code": "INVALID_SESSION",
            "message": "uuid가 등록되지 않은 세션. uuid 재생성 후 재전송 필요.",
            "timestamp": "2026-05-26T00:00:00Z"
        }}}}
    }
)
async def receive_emergency(data: BiometricEmergency, userId: str = Header(...), db: Session = Depends(get_db)):
    # samples 10개 검증
    if len(data.samples) > 10:
        return JSONResponse(status_code=400, content={
            "type": "error",
            "uuid": data.uuid,
            "code": "INVALID_BATCH_SIZE",
            "message": f"긴급 채널 samples 배열 크기는 최대 10개. 수신 크기: {len(data.samples)}",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })

    # 세션 존재 여부 확인
    existing = db.get(BiometricSession, data.uuid)
    if not existing:
        return JSONResponse(status_code=400, content={
            "type": "error",
            "uuid": data.uuid,
            "code": "INVALID_SESSION",
            "message": "uuid가 등록되지 않은 세션. uuid 재생성 후 재전송 필요.",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })

    # 샘플 저장
    for s in data.samples:
        sample = Sample(uuid=data.uuid, ts=s.ts, acc_x=s.acc_x, acc_y=s.acc_y, acc_z=s.acc_z, lat=s.gps.lat, lon=s.gps.lon)
        db.add(sample)

    # 심박수 저장
    for hr in data.heart_rates:
        heart_rate = HeartRate(uuid=data.uuid, start_time=hr.start_time, end_time=hr.end_time, value=hr.value)
        db.add(heart_rate)

    # 혈중산소 저장
    for bo in data.blood_oxygens:
        blood_oxygen = BloodOxygen(uuid=data.uuid, start_time=bo.start_time, end_time=bo.end_time, value=bo.value)
        db.add(blood_oxygen)

    # 걸음수 저장
    for st in data.steps:
        step = Step(uuid=data.uuid, start_time=st.start_time, end_time=st.end_time, value=st.value)
        db.add(step)

    db.commit()

    # 트리거 GPS 위치로 아이나비에 즉시 결과 전송
    await send_result(
        uuid=data.uuid,
        user_id=userId,
        lat=data.gps_at_trigger.lat,
        lon=data.gps_at_trigger.lon
    )

    return {"status": "ok", "uuid": data.uuid, "trigger_type": data.trigger_type}