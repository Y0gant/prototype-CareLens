import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from database_config import init_db, close_db
from logging_config import configure_logging
from routers import encounter_router, feedback_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = init_db()
    logger.info("Application started, DB connected")
    yield
    await close_db()
    logger.info("Application shutting down")


app = FastAPI(lifespan=lifespan)

# ====== Routers Here ======
app.include_router(encounter_router.router)
app.include_router(feedback_router.router)

# ==== Logging here ====
configure_logging()
logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    return {"message": "Welcome"}


@app.get("/health")
async def root_health():
    return {"status": "running..."}
