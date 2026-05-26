from pydantic import BaseModel
from typing import List, Optional

class GPS(BaseModel):
    lat: float
    lon: float

class Sample(BaseModel):
    ts: str
    acc_x: float
    acc_y: float
    acc_z: float
    gps: GPS

class HeartRate(BaseModel):
    start_time: str
    end_time: str
    value: int

class BloodOxygen(BaseModel):
    start_time: str
    end_time: str
    value: int

class Step(BaseModel):
    start_time: str
    end_time: str
    value: int

# DTO-1 일반 채널
class BiometricNormal(BaseModel):
    uuid: str
    samples: List[Sample]
    heart_rates: Optional[List[HeartRate]] = []
    blood_oxygens: Optional[List[BloodOxygen]] = []
    steps: List[Step]

# DTO-1 긴급 채널
class BiometricEmergency(BaseModel):
    uuid: str
    trigger_type: str  # T-1(낙상), T-2(심박급변), T-3(장시간정지)
    trigger_ts: str
    trigger_value: float
    gps_at_trigger: GPS
    samples: List[Sample]
    heart_rates: Optional[List[HeartRate]] = []
    blood_oxygens: Optional[List[BloodOxygen]] = []
    steps: Optional[List[Step]] = []