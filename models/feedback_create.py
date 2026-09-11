from pydantic import BaseModel


class FeedbackCreate(BaseModel):
    encounter_id: str
    complaint_text: str
    department: str
