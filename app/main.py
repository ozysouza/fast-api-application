from fastapi import FastAPI
from contextlib import asynccontextmanager

from .database import create_db_and_tables
from app.routers import post, users

ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables at app startup
    create_db_and_tables()
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()


app = FastAPI(lifespan=lifespan)

app.include_router(post.router)
app.include_router(users.router)
