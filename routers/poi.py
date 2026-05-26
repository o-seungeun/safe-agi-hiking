from fastapi import APIRouter
from schemas.poi import POIData

router = APIRouter()

@router.post("/poi",
    summary="POI 데이터 수신",
    description="쉼터, 위험구간, 음수대 등 POI 데이터 수신. DTO-2와 함께 초기 1회 전송 후 변경 시 갱신."
)
async def receive_poi(data: POIData):
    return {"status": "ok", "mountain_id": data.mountain_id}