from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict
from datetime import datetime

class JobDescriptionBase(BaseModel):
    title: str
    required_skills: List[str]
    min_experience: int
    qualifications: List[str]
    responsibilities: str

class JobDescriptionCreate(JobDescriptionBase):
    pass

class JobDescription(JobDescriptionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Changed from orm_mode = True

class CandidateBase(BaseModel):
    name: str
    email: EmailStr
    skills: List[str]
    experience: Dict[str, str]
    education: List[Dict[str, str]]

class CandidateCreate(CandidateBase):
    pass

class Candidate(CandidateBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Changed from orm_mode = True

class ApplicationBase(BaseModel):
    job_id: int
    candidate_id: int
    match_score: float
    status: str

class ApplicationCreate(ApplicationBase):
    pass

class Application(ApplicationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Changed from orm_mode = True

class InterviewBase(BaseModel):
    application_id: int
    scheduled_time: datetime
    interview_type: str
    notes: Optional[str] = None

class InterviewCreate(InterviewBase):
    pass

class Interview(InterviewBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True  # Changed from orm_mode = True