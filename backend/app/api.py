from fastapi import APIRouter
from pymongo import MongoClient

router = APIRouter()
client = MongoClient("mongodb://mongodb:27017")
db = client.weather
collection = db.sunlight

@router.get("/sunlight")
def get_sunlight():
    data = list(collection.find({}, {"_id": 0}))
    return data