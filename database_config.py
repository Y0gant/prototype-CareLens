import logging
import os

from dotenv import load_dotenv
from fastapi import Request
from pymongo import AsyncMongoClient

logger = logging.getLogger(__name__)

load_dotenv()

DATABASE_URL = os.getenv("MONGODB_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env file.")

_client: AsyncMongoClient | None = None


def init_db():
    global _client
    _client = AsyncMongoClient(DATABASE_URL)
    logger.info("MongoDB client initialized.")
    return _client["care_lens"]


async def close_db():
    if _client is not None:
        await _client.close()
        logger.info("MongoDB client closed.")


def get_db(request: Request):
    return request.app.state.db
