from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.poi import POIData
from schemas.common import CommonResponse
from models.terrain import Mountain, Poi
from database import get_db
from utils import success_response, COMMON_RESPONSES

router = APIRouter()

@router.post("/poi",
    response_model=CommonResponse,
    summary="POI 데이터 수신",
    description="쉼터, 위험구간 등 POI 데이터 수신. 초기 1회 전송 후 변경 시 갱신.",
    responses=COMMON_RESPONSES
)
async def receive_poi(data: POIData, db: Session = Depends(get_db)):
    # Mountain 없으면 생성
    mountain = db.get(Mountain, data.mountain_id)
    if not mountain:
        db.add(Mountain(
            mountain_id=data.mountain_id,
            mountain_name=data.mountain_name,
            data_version=data.version
        ))
        db.flush()

    # POI upsert
    for p in data.pois:
        poi = db.get(Poi, p.poi_id)
        if not poi:
            db.add(Poi(
                poi_id=p.poi_id,
                mountain_id=data.mountain_id,
                poi_name=p.poi_name,
                cate_cd=p.cate_cd,
                lat=p.lat,
                lon=p.lon,
                altitude_m=p.altitude_m,
                description=p.desc
            ))
        else:
            poi.poi_name = p.poi_name
            poi.cate_cd = p.cate_cd
            poi.lat = p.lat
            poi.lon = p.lon
            poi.altitude_m = p.altitude_m
            poi.description = p.desc
    db.commit()

    return success_response()
