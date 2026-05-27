from fastapi import APIRouter
from schemas.poi import POIData
from schemas.common import CommonResponse
from utils import success_response, COMMON_RESPONSES

router = APIRouter()

@router.post("/poi",
    response_model=CommonResponse,
    summary="POI 데이터 수신",
    description="쉼터, 위험구간 등 POI 데이터 수신. 초기 1회 전송 후 변경 시 갱신.",
    responses=COMMON_RESPONSES
)
async def receive_poi(data: POIData):
    return success_response()