from fastapi import APIRouter
from schemas.trail import TrailNetwork

router = APIRouter()

@router.post("/trail",
    summary="등산로 네트워크 데이터 수신",
    description="100대 명산 등산로 링크, 노드, GPX 데이터 수신. 초기 1회 전송 후 변경 시 갱신."
)
async def receive_trail(data: TrailNetwork):
    return {"status": "ok", "mountain_id": data.mountain_id}