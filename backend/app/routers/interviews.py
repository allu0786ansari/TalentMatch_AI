from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..database import get_db
from .. import models, schemas
from ..utils.email import send_interview_invitation

router = APIRouter()

@router.post("/schedule", response_model=schemas.Interview)
async def schedule_interview(
    interview: schemas.InterviewCreate,
    db: Session = Depends(get_db)
):
    # Check if application exists
    application = db.query(models.Application).filter(
        models.Application.id == interview.application_id
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    # Create interview
    db_interview = models.Interview(
        **interview.dict(),
        status="scheduled"
    )
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)

    # Send interview invitation
    await send_interview_invitation(db_interview, application)
    
    return db_interview

@router.get("/{application_id}", response_model=schemas.Interview)
async def get_interview(application_id: int, db: Session = Depends(get_db)):
    interview = db.query(models.Interview).filter(
        models.Interview.application_id == application_id
    ).first()
    
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    return interview

@router.put("/{interview_id}", response_model=schemas.Interview)
async def update_interview(
    interview_id: int,
    interview_update: schemas.InterviewCreate,
    db: Session = Depends(get_db)
):
    interview = db.query(models.Interview).filter(
        models.Interview.id == interview_id
    ).first()
    
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    for key, value in interview_update.dict().items():
        setattr(interview, key, value)
    
    db.commit()
    db.refresh(interview)
    return interview