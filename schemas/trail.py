# DTO-2 스키마 코드

from pydantic import BaseModel
from typing import List, Optional

class Geometry(BaseModel):
    lat: float
    lon: float

class Link(BaseModel):
    link_id: str
    start_node: str
    end_node: str
    length_m: float
    slope_deg: float
    course_type: str
    popular: str
    legal: str
    surface: str
    difficulty: int
    geometry: List[Geometry]

class Node(BaseModel):
    node_id: str
    lat: float
    lon: float
    altitude_m: Optional[float] = None
    node_type: str

class TrailNetwork(BaseModel):
    mountain_id: str
    mountain_name: str
    version: str
    coord_system: str
    gpx_file: Optional[str] = None
    links: List[Link]
    nodes: List[Node]