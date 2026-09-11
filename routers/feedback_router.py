from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from database_config import get_db
from models.feedback_create import FeedbackCreate
from models.feedback_out import FeedbackOut

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("/")
async def create_feedback(feedback: FeedbackCreate, db=Depends(get_db)):
    feedback_dict = feedback.model_dump()
    feedback_dict["created_at"] = datetime.now(timezone.utc)
    result = await db["feedback"].insert_one(feedback_dict)
    return {"inserted_id": str(result.inserted_id), "feedback": feedback}


@router.get("/{feedback_id}")
async def get_feedback(feedback_id: str, db=Depends(get_db)):
    if not ObjectId.is_valid(feedback_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    doc = await db["feedback"].find_one({"_id": ObjectId(feedback_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Item not found")

    doc["_id"] = str(doc["_id"])

    return FeedbackOut(**doc)


@router.get("/")
async def list_feedback(encounter_id: str | None = None, db=Depends(get_db)):
    query = {"encounter_id": encounter_id} if encounter_id else {}
    items = []
    cursor = db["feedback"].find(query)
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        items.append(FeedbackOut(**doc))
    return items
