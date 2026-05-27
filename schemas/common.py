from pydantic import BaseModel

class CommonResponse(BaseModel):
    code: str
    msg: str