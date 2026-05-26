# DTO-3 스키마 코드

from pydantic import BaseModel
from typing import List, Optional

class POI(BaseModel):
    poi_id: int
    poi_name: str
    cate_cd: str
    lat: float
    lon: float
    altitude_m: Optional[float] = None
    desc: Optional[str] = None

class POIData(BaseModel):
    mountain_id: str
    mountain_name: str
    version: str
    pois: List[POI]