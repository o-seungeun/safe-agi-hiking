from fastapi import APIRouter, Header
from schemas.history import HikingHistory

router = APIRouter()

@router.post("/history",
    summary="등반 이력 데이터 수신",
    description="사용자 과거 등반 세션 이력 데이터 수신. MAML 모델 학습용. 초기 대량 전송 후 월 1회 또는 일정 세션 누적 시 갱신."
)
async def receive_history(data: HikingHistory, userId: str = Header(...)):
    return {"status": "ok", "userId": userId, "sessions": len(data.sessions)}