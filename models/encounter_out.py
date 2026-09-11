from datetime import datetime

from pydantic import BaseModel, Field


class EncounterOut(BaseModel):
    id: str = Field(alias="_id")
    department: str
    admission_date: datetime
    discharge_date: datetime
    discharge_delay_hrs: float
    occupancy_pct: float
    insurance_delay_hrs: float
    patient_age: int
    patient_gender: str

    class Config:
        populate_by_name = True
