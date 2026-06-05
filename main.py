from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routers import biometric, trail, poi, history
from schemas.common import CommonResponse
from utils import success_response

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
    },
    {
        "name": "default",
        "description": "서버 상태 확인"
    }
]

app = FastAPI(
    title="S.A.F.E. AI Backend API",
    description="S.A.F.E. 산행 안전 AI 플랫폼",
    version="1.0",
    openapi_tags=tags_metadata
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "code": "422",
            "msg": "유효성 검사 실패",
            "detail": exc.errors()
        }
    )

app.include_router(biometric.router, prefix="/sookmyung", tags=["Biometric"])
app.include_router(trail.router, prefix="/sookmyung", tags=["Trail & POI"])
app.include_router(poi.router, prefix="/sookmyung", tags=["Trail & POI"])
app.include_router(history.router, prefix="/sookmyung", tags=["History"])

@app.get("/",
    response_model=CommonResponse,
    summary="Health Check",
    responses={
        200: {"description": "성공"}
    },
    tags=["default"]
)
def read_root():
    return success_response()