import json
import logging
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
logger = logging.getLogger(__name__)

from models.operations_answer import OperationsAnswer

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def ask_operations_question(question: str, aggregation_data: list[dict]) -> str | None:
    prompt = f"""You are a hospital operations analyst.
Given the question and the aggregated department data below, answer using ONLY the data provided.

Question: {question}

Data:
{json.dumps(aggregation_data, default=str)}
"""
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=OperationsAnswer,
            )
        )
        return str(response.parsed)

    except Exception as e:
        logger.warning(f"Got Invalid Answer From Gemini: {e}")
        raise
