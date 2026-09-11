from datetime import datetime
from typing import TypedDict


class FeedbackDocument(TypedDict):
    encounter_id: str
    complaint_text: str
    department: str
    created_at: datetime
