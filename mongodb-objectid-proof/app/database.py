"""MongoDB database connection and utilities."""

from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from typing import Optional

# MongoDB connection settings
MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "objectid_proof"
COLLECTION_NAME = "documents"

# Create MongoDB client
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]


def get_collection():
    """Get the documents collection."""
    return collection


def objectid_to_dict(doc: dict) -> dict:
    """Convert a document with ObjectId to a serializable dict with generation_time."""
    object_id: ObjectId = doc["_id"]
    generation_time: datetime = object_id.generation_time
    
    return {
        "_id": str(object_id),
        "generation_time": generation_time.isoformat(),
        "generation_time_timestamp": generation_time.timestamp(),
        **{k: v for k, v in doc.items() if k != "_id"}
    }
