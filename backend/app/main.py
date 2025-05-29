from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware

from app import api  # 👈 import your api.py

app = FastAPI()

# MongoDB setup
app = FastAPI()

# MongoDB async setup
client = AsyncIOMotorClient("mongodb://mongodb:27017")
app.state.db = client.weather


# Expose DB as module-level (for api.py to import)
import sys
sys.modules[__name__].db = db

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api.router)
