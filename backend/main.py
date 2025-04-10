from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Import local modules
from app.routers import jobs, candidates, matches, interviews
from app.database import engine
from app.models import Base
from app.config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="TalentMatch AI",
    description="A Multi-Agent System for Streamlining Recruitment Processes",
    version="1.0.0"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    jobs.router,
    prefix="/api/v1/jobs",
    tags=["jobs"]
)

app.include_router(
    candidates.router,
    prefix="/api/v1/candidates",
    tags=["candidates"]
)

app.include_router(
    matches.router,
    prefix="/api/v1/matches",
    tags=["matches"]
)

app.include_router(
    interviews.router,
    prefix="/api/v1/interviews",
    tags=["interviews"]
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to TalentMatch AI API",
        "version": settings.VERSION,
        "docs_url": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "system": "operational"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )