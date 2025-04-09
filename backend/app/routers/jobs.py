from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas
from app.utils.matching import process_job_description

router = APIRouter()

@router.post("/", response_model=schemas.JobDescription)
async def create_job(job: schemas.JobDescriptionCreate, db: Session = Depends(get_db)):
    db_job = models.JobDescription(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/", response_model=List[schemas.JobDescription])
async def get_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = db.query(models.JobDescription).offset(skip).limit(limit).all()
    return jobs

@router.get("/{job_id}", response_model=schemas.JobDescription)
async def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.JobDescription).filter(models.JobDescription.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.delete("/{job_id}")
async def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.JobDescription).filter(models.JobDescription.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"message": "Job deleted successfully"}