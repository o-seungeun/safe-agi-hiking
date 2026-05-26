from fastapi import FastAPI
from routers import biometric, trail, poi, history

tags_metadata = [
    {
        "name": "Biometric",
        "description": "웨어러블(워치) 생체 데이터"
    },
    {
        "name": "Trail & POI",
        "description": "등산로 네트워크, POI 데이터"
    },
    {
        "name": "History",
        "description": "사용자 등반 이력 데이터"
    }
]

app = FastAPI(
    title="S.A.F.E. AI Backend API",
    description="S.A.F.E. 산행 안전 AI 플랫폼",
    version="1.0",
    openapi_tags=tags_metadata
)

app.include_router(biometric.router, prefix="/sookmyung", tags=["Biometric"])
app.include_router(trail.router, prefix="/sookmyung", tags=["Trail & POI"])
app.include_router(poi.router, prefix="/sookmyung", tags=["Trail & POI"])
app.include_router(history.router, prefix="/sookmyung", tags=["History"])

@app.get("/")
def read_root():
    return {"message": "SAFE API 서버 작동 중"}