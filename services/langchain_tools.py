from langchain_core.tools import tool
from pymongo import AsyncMongoClient

from services.AggregationService import AggregationService

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "care_lens"


@tool
async def get_department_delay_summary_tool() -> list[dict]:
    """Returns average discharge delay, insurance delay, and occupancy per department."""
    client = AsyncMongoClient(MONGO_URI)
    db = client[DB_NAME]
    service = AggregationService(db)
    return await service.get_department_delay_summary()
