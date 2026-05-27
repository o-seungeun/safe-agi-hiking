from fastapi import APIRouter, Header
from schemas.history import HikingHistory
from schemas.common import CommonResponse
from utils import success_response, COMMON_RESPONSES

router = APIRouter()

@router.post("/history",
    response_model=CommonResponse,
    summary="등반 이력 데이터 수신",
    description="사용자 과거 등반 세션 이력 데이터 수신. 초기 대량 전송 후 월 1회 또는 일정 세션 누적 시 갱신.",
    responses=COMMON_RESPONSES
)
async def receive_history(data: HikingHistory, userId: str = Header(...)):
    return success_response()