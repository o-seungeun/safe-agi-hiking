from fastapi.responses import JSONResponse

def success_response(msg="성공"):
    return {
        "code": "0",
        "msg": msg
    }

def error_response(code="100", msg="요청 처리 실패", status_code=400):
    return JSONResponse(status_code=status_code, content={
        "code": code,
        "msg": msg
    })

COMMON_RESPONSES = {
    200: {"description": "성공"},
    422: {
        "description": "유효성 검사 실패",
        "content": {"application/json": {"example": {
            "code": "422",
            "msg": "유효성 검사 실패",
            "detail": []
        }}}
    }
}