"""FastAPI application for MongoDB ObjectId DateTime Proof."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router as documents_router

app = FastAPI(
    title="MongoDB ObjectId DateTime Proof",
    description="""
    This API demonstrates that MongoDB ObjectIds contain embedded timestamps.
    
    Each ObjectId's first 4 bytes represent the Unix timestamp when it was created.
    Using PyMongo's bson module, we can extract this `generation_time` to prove
    that documents inserted later have ObjectIds with more recent timestamps.
    """,
    version="1.0.0"
)

# Add CORS middleware for Jupyter notebook access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(documents_router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "MongoDB ObjectId DateTime Proof API",
        "docs": "/docs",
        "endpoints": {
            "POST /documents": "Insert a single document",
            "POST /documents/batch": "Insert multiple documents with optional delay",
            "GET /documents": "Get all documents with ObjectId timestamps",
            "DELETE /documents": "Delete all documents",
            "GET /documents/compare-first-last": "Compare first and last document timestamps"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    from .database import client
    try:
        client.admin.command('ping')
        return {"status": "healthy", "mongodb": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "mongodb": str(e)}
