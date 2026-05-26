import httpx
from datetime import datetime

AIRNAVI_SERVER_URL = "http://3.37.223.154:1447/sookmyung/result"  # 아이나비 개발 서버

async def send_result(uuid: str, user_id: str, lat: float, lon: float):
    # 더미 결과 (모델 완성 후 ml/maml.py 결과로 교체 예정)
    payload = {
        "type": "inference_result",
        "uuid": uuid,
        "userId": user_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_location": {"lat": lat, "lon": lon},
        "course_recommendation": None,
        "risk": {
            "e1_biometric": 0.1,
            "e2_combined": 0.2,
            "representative": 0.2
        },
        "fatigue": {
            "state": "정상",
            "confidence": 0.9,
            "nearest_shelter": None
        },
        "descent_warning": {
            "required": False,
            "reason": None,
            "remaining_daylight_min": 180
        },
        "alerts": []
    }

    async with httpx.AsyncClient() as client:
        await client.post(AIRNAVI_SERVER_URL, json=payload)