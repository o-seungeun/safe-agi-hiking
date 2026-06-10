from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.trail import TrailNetwork
from schemas.common import CommonResponse
from models.terrain import Mountain, TrailNode, TrailLink
from database import get_db
from utils import success_response, COMMON_RESPONSES

router = APIRouter()

@router.post("/trail",
    response_model=CommonResponse,
    summary="등산로 네트워크 데이터 수신",
    description="100대 명산 등산로 링크, 노드, GPX 데이터 수신. 초기 1회 전송 후 변경 시 갱신.",
    responses=COMMON_RESPONSES
)
async def receive_trail(data: TrailNetwork, db: Session = Depends(get_db)):
    # Mountain upsert
    mountain = db.get(Mountain, data.mountain_id)
    if not mountain:
        mountain = Mountain(
            mountain_id=data.mountain_id,
            mountain_name=data.mountain_name,
            data_version=data.version,
            coord_system=data.coord_system,
            gpx_file=data.gpx_file
        )
        db.add(mountain)
    else:
        mountain.mountain_name = data.mountain_name
        mountain.data_version = data.version
        mountain.gpx_file = data.gpx_file
    db.flush()

    # Nodes upsert
    for n in data.nodes:
        node = db.get(TrailNode, n.node_id)
        if not node:
            db.add(TrailNode(
                node_id=n.node_id,
                mountain_id=data.mountain_id,
                lat=n.lat,
                lon=n.lon,
                altitude_m=n.altitude_m,
                node_type=n.node_type
            ))
        else:
            node.lat = n.lat
            node.lon = n.lon
            node.altitude_m = n.altitude_m
    db.flush()

    # Links upsert
    for l in data.links:
        link = db.get(TrailLink, l.link_id)
        if not link:
            db.add(TrailLink(
                link_id=l.link_id,
                mountain_id=data.mountain_id,
                start_node_id=l.start_node,
                end_node_id=l.end_node,
                length_m=l.length_m,
                slope_deg=l.slope_deg,
                course_type=l.course_type,
                popular=l.popular,
                legal=l.legal,
                surface=l.surface,
                difficulty=l.difficulty,
                geometry=[g.model_dump() for g in l.geometry]
            ))
        else:
            link.length_m = l.length_m
            link.slope_deg = l.slope_deg
            link.difficulty = l.difficulty
    db.commit()

    return success_response()
