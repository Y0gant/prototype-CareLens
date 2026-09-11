from datetime import datetime

from pydantic import BaseModel, Field


class FeedbackOut(BaseModel):
    id: str = Field(alias="_id")
    encounter_id: str
    complaint_text: str
    department: str
    created_at: datetime

    class Config:
        populate_by_name = True
