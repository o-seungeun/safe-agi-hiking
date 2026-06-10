from pydantic import BaseModel, Field
from typing import List, Optional

class GPS(BaseModel):
    lat: float = Field(example=37.5665)
    lon: float = Field(example=126.9780)

class Sample(BaseModel):
    ts: str = Field(example="2026-06-10T08:00:01Z")
    acc_x: float = Field(example=0.12)
    acc_y: float = Field(example=-9.78)
    acc_z: float = Field(example=0.34)
    gps: GPS

class HeartRate(BaseModel):
    start_time: str = Field(example="2026-06-10T08:00:00Z")
    end_time: str = Field(example="2026-06-10T08:00:10Z")
    value: int = Field(example=88)

class BloodOxygen(BaseModel):
    start_time: str = Field(example="2026-06-10T08:00:00Z")
    end_time: str = Field(example="2026-06-10T08:01:00Z")
    value: int = Field(example=97)

class Step(BaseModel):
    start_time: str = Field(example="2026-06-10T08:00:00Z")
    end_time: str = Field(example="2026-06-10T08:01:00Z")
    value: int = Field(example=85)

# DTO-1 일반 채널
class BiometricNormal(BaseModel):
    uuid: str = Field(example="sess_20260610_001")
    samples: List[Sample]
    heart_rates: Optional[List[HeartRate]] = []
    blood_oxygens: Optional[List[BloodOxygen]] = []
    steps: List[Step]

# DTO-1 긴급 채널
class BiometricEmergency(BaseModel):
    uuid: str = Field(example="sess_20260610_001")
    trigger_type: str = Field(example="T-1")  # T-1(낙상), T-2(심박급변), T-3(장시간정지)
    trigger_ts: str = Field(example="2026-06-10T08:05:32Z")
    trigger_value: float = Field(example=23.4)
    gps_at_trigger: GPS
    samples: List[Sample]
    heart_rates: Optional[List[HeartRate]] = []
    blood_oxygens: Optional[List[BloodOxygen]] = []
    steps: Optional[List[Step]] = []