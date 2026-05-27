from fastapi import APIRouter
from schemas.trail import TrailNetwork
from schemas.common import CommonResponse
from utils import success_response, COMMON_RESPONSES

router = APIRouter()

@router.post("/trail",
    response_model=CommonResponse,
    summary="등산로 네트워크 데이터 수신",
    description="100대 명산 등산로 링크, 노드, GPX 데이터 수신. 초기 1회 전송 후 변경 시 갱신.",
    responses=COMMON_RESPONSES
)
async def receive_trail(data: TrailNetwork):
    return success_response()