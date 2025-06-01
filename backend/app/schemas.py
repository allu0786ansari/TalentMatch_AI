from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict
from datetime import datetime
from pydantic.config import ConfigDict


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

    model_config = ConfigDict(from_attributes=True)  # Updated

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

    model_config = ConfigDict(from_attributes=True)  # Updated

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

    model_config = ConfigDict(from_attributes=True)  # Updated

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

    model_config = ConfigDict(from_attributes=True)  # Updated

# Authentication-related schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token_data: Dict[str, str]
    new_password: str