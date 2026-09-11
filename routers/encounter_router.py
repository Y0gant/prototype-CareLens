from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from database_config import get_db
from models.encounter_create import EncounterCreate
from models.encounter_out import EncounterOut

router = APIRouter(prefix="/encounters", tags=["encounters"])


@router.post("/")
async def create_encounter(encounter: EncounterCreate, db=Depends(get_db)):
    encounter_dict = encounter.model_dump()
    result = await db["encounters"].insert_one(encounter_dict)
    return {"inserted_id": str(result.inserted_id), "encounter": encounter_dict}


@router.get("/{encounter_id}")
async def get_encounter(encounter_id: str, db=Depends(get_db)):
    if not ObjectId.is_valid(encounter_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    doc = await db["encounters"].find_one({"_id": ObjectId(encounter_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Item not found")

    doc["_id"] = str(doc["_id"])

    return EncounterOut(**doc)


@router.get("/")
async def list_encounters(department: str | None = None, db=Depends(get_db)):
    query = {"department": department} if department else {}
    items = []
    cursor = db["encounters"].find(query)
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        items.append(EncounterOut(**doc))
    return items
