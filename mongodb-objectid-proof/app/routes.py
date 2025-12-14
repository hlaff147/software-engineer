"""API routes for document operations."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Any
import time

from .database import get_collection, objectid_to_dict

router = APIRouter(prefix="/documents", tags=["documents"])


class DocumentCreate(BaseModel):
    """Request model for creating a document."""
    name: str
    data: Optional[dict] = None


class BatchInsertRequest(BaseModel):
    """Request model for batch document insertion."""
    count: int = 10
    delay_ms: Optional[int] = 0  # Delay between insertions in milliseconds
    prefix: str = "doc"


class DocumentResponse(BaseModel):
    """Response model for a document with ObjectId info."""
    _id: str
    generation_time: str
    generation_time_timestamp: float
    name: str
    data: Optional[dict] = None
    insertion_order: Optional[int] = None


@router.post("", response_model=dict)
async def create_document(document: DocumentCreate):
    """Insert a single document and return its ObjectId with generation time."""
    collection = get_collection()
    
    doc_data = {
        "name": document.name,
        "data": document.data or {}
    }
    
    result = collection.insert_one(doc_data)
    inserted_doc = collection.find_one({"_id": result.inserted_id})
    
    return objectid_to_dict(inserted_doc)


@router.post("/batch", response_model=List[dict])
async def create_batch_documents(request: BatchInsertRequest):
    """
    Insert multiple documents with optional delay between insertions.
    
    This is useful to demonstrate that ObjectIds created at different times
    have different generation_time values.
    """
    collection = get_collection()
    inserted_docs = []
    
    for i in range(request.count):
        doc_data = {
            "name": f"{request.prefix}_{i+1}",
            "insertion_order": i + 1,
            "data": {"batch_insert": True, "index": i}
        }
        
        result = collection.insert_one(doc_data)
        inserted_doc = collection.find_one({"_id": result.inserted_id})
        inserted_docs.append(objectid_to_dict(inserted_doc))
        
        # Add delay if specified
        if request.delay_ms and request.delay_ms > 0 and i < request.count - 1:
            time.sleep(request.delay_ms / 1000.0)
    
    return inserted_docs


@router.get("", response_model=List[dict])
async def get_all_documents():
    """
    Retrieve all documents sorted by _id (which inherently sorts by creation time).
    
    Returns each document with its ObjectId and extracted generation_time,
    proving that earlier ObjectIds have earlier timestamps.
    """
    collection = get_collection()
    documents = list(collection.find().sort("_id", 1))
    
    return [objectid_to_dict(doc) for doc in documents]


@router.delete("")
async def delete_all_documents():
    """Delete all documents from the collection."""
    collection = get_collection()
    result = collection.delete_many({})
    
    return {
        "message": "All documents deleted",
        "deleted_count": result.deleted_count
    }


@router.get("/compare-first-last")
async def compare_first_last():
    """
    Compare the first and last inserted documents.
    
    This endpoint clearly demonstrates that the last inserted document
    has a more recent ObjectId generation time than the first one.
    """
    collection = get_collection()
    
    # Get first document (earliest ObjectId)
    first_doc = collection.find_one(sort=[("_id", 1)])
    
    # Get last document (latest ObjectId)
    last_doc = collection.find_one(sort=[("_id", -1)])
    
    if not first_doc or not last_doc:
        raise HTTPException(status_code=404, detail="No documents found")
    
    first = objectid_to_dict(first_doc)
    last = objectid_to_dict(last_doc)
    
    time_diff_seconds = last["generation_time_timestamp"] - first["generation_time_timestamp"]
    
    return {
        "first_document": first,
        "last_document": last,
        "time_difference_seconds": time_diff_seconds,
        "proof": "The last inserted ObjectId has a more recent timestamp" if time_diff_seconds >= 0 else "Unexpected: first is newer"
    }
