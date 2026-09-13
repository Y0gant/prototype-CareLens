import random
from datetime import datetime, timedelta

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["care_lens"]

DEPARTMENTS = ["Orthopedics", "Cardiology", "Neurology", "General Medicine", "Pediatrics"]

BASELINE = {
    "occupancy_pct": (60, 80),
    "discharge_delay_hrs": (1, 6),
    "insurance_delay_hrs": (2, 10),
}

ANOMALY = {
    "Orthopedics": {
        "occupancy_pct": (88, 98),
        "discharge_delay_hrs": (10, 24),
        "insurance_delay_hrs": (18, 40),
    }
}

# Complaint text templates — the "category" signal now lives in wording, not a field.
# This matters for Day 8 RAG: cosine similarity needs distinguishable text, not a label.
GOOD_COMPLAINTS = [
    "Staff were courteous and the room was clean.",
    "Communication from the care team was clear throughout the stay.",
    "Minor wait at check-in but overall a smooth experience.",
]

BAD_COMPLAINTS = [
    "Waited over {n} hours past the expected discharge time with no update.",
    "Insurance approval took days, no one could tell us why it was delayed.",
    "Ward felt overcrowded, staff seemed stretched too thin to check in regularly.",
    "Billing department gave three different figures for the same procedure.",
    "Discharge paperwork sat untouched for hours after we were told we could leave.",
]


def gen_encounter(dept, i):
    ranges = ANOMALY.get(dept, BASELINE)
    admission = datetime(2026, 1, 1) + timedelta(days=random.randint(0, 240))
    discharge_delay = round(random.uniform(*ranges["discharge_delay_hrs"]), 1)
    return {
        "department": dept,
        "admission_date": admission,
        "discharge_date": admission + timedelta(hours=48 + discharge_delay),
        "discharge_delay_hrs": discharge_delay,
        "occupancy_pct": round(random.uniform(*ranges["occupancy_pct"]), 1),
        "insurance_delay_hrs": round(random.uniform(*ranges["insurance_delay_hrs"]), 1),
        "patient_age": random.randint(5, 85),
        "patient_gender": random.choice(["M", "F"]),
    }


def gen_feedback(encounter_id, dept, is_anomaly):
    if is_anomaly:
        template = random.choice(BAD_COMPLAINTS)
        text = template.format(n=random.randint(8, 20)) if "{n}" in template else template
    else:
        text = random.choice(GOOD_COMPLAINTS)

    return {
        "encounter_id": encounter_id,
        "complaint_text": text,
        "department": dept,
        "created_at": datetime.now(),
    }


def generate():
    db.encounters.delete_many({})
    db.feedback.delete_many({})

    encounter_docs = []
    for dept in DEPARTMENTS:
        count = 80 if dept != "Orthopedics" else 100
        for i in range(count):
            encounter_docs.append(gen_encounter(dept, i))

    result = db.encounters.insert_many(encounter_docs)

    feedback_docs = []
    for enc_id, enc in zip(result.inserted_ids, encounter_docs):
        if random.random() < 0.4:
            is_anomaly = enc["department"] == "Orthopedics"
            feedback_docs.append(gen_feedback(str(enc_id), enc["department"], is_anomaly))

    if feedback_docs:
        db.feedback.insert_many(feedback_docs)

    print(f"Inserted {len(encounter_docs)} encounters, {len(feedback_docs)} feedback docs")


if __name__ == "__main__":
    generate()
