from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas
from ..utils.matching import calculate_match_score

router = APIRouter()

@router.post("/match/{job_id}", response_model=List[schemas.Application])
async def match_candidates_for_job(
    job_id: int, 
    min_score: float = 0.8,
    db: Session = Depends(get_db)
):
    # Get job description
    job = db.query(models.JobDescription).filter(models.JobDescription.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Get all candidates
    candidates = db.query(models.Candidate).all()
    matched_applications = []

    for candidate in candidates:
        # Calculate match score
        score = calculate_match_score(job, candidate)
        
        if score >= min_score:
            application = models.Application(
                job_id=job_id,
                candidate_id=candidate.id,
                match_score=score,
                status="pending"
            )
            db.add(application)
            matched_applications.append(application)

    db.commit()
    return matched_applications

@router.get("/applications/{job_id}", response_model=List[schemas.Application])
async def get_job_applications(
    job_id: int,
    status: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Application).filter(models.Application.job_id == job_id)
    
    if status:
        query = query.filter(models.Application.status == status)
    
    applications = query.all()
    return applications

@router.put("/applications/{application_id}", response_model=schemas.Application)
async def update_application_status(
    application_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    application = db.query(models.Application).filter(
        models.Application.id == application_id
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    application.status = status
    db.commit()
    db.refresh(application)
    return application