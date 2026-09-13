from typing import Any


class AggregationService:
    def __init__(self, db):
        self.encounters = db["encounters"]
        self.feedback = db["feedback"]

    async def get_department_delay_summary(self) -> list[dict[str, Any]]:
        """
        Query 1: average discharge/insurance delay and occupancy per department,
        sorted worst-first by discharge delay.
        """
        pipeline = [
            {"$group": {
                "_id": "$department",
                "avg_discharge_delay": {"$avg": "$discharge_delay_hrs"},
                "avg_insurance_delay": {"$avg": "$insurance_delay_hrs"},
                "avg_occupancy": {"$avg": "$occupancy_pct"},
                "encounter_count": {"$sum": 1},
            }},
            {"$sort": {"avg_discharge_delay": -1}},
        ]
        cursor = await self.encounters.aggregate(pipeline)
        return [doc async for doc in cursor]

    async def get_feedback_volume_by_department(self) -> list[dict[str, Any]]:
        """
        Query 2: feedback count per department with a capped sample of raw
        complaint text (no category/rating field exists on this schema).
        """
        pipeline = [
            {"$group": {
                "_id": "$department",
                "feedback_count": {"$sum": 1},
                "sample_complaints": {"$push": "$complaint_text"},
            }},
            {"$project": {
                "feedback_count": 1,
                "sample_complaints": {"$slice": ["$sample_complaints", 3]},
            }},
            {"$sort": {"feedback_count": -1}},
        ]
        cursor = await self.feedback.aggregate(pipeline)
        return [doc async for doc in cursor]

    async def get_critical_departments(
            self,
            discharge_delay_threshold: float = 8.0,
            insurance_delay_threshold: float = 15.0,
            occupancy_threshold: float = 85.0,
    ) -> list[dict[str, Any]]:
        """
        Query 3: departments exceeding all three thresholds at once —
        thresholds parameterized rather than hardcoded so this is reusable,
        not a one-off script.
        """
        pipeline = [
            {"$group": {
                "_id": "$department",
                "avg_discharge_delay": {"$avg": "$discharge_delay_hrs"},
                "avg_insurance_delay": {"$avg": "$insurance_delay_hrs"},
                "avg_occupancy": {"$avg": "$occupancy_pct"},
            }},
            {"$match": {
                "avg_discharge_delay": {"$gt": discharge_delay_threshold},
                "avg_insurance_delay": {"$gt": insurance_delay_threshold},
                "avg_occupancy": {"$gt": occupancy_threshold},
            }},
        ]
        cursor = await self.encounters.aggregate(pipeline)
        return [doc async for doc in cursor]
