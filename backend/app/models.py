from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime, timezone  # Import timezone for UTC

class JobDescription(Base):
    __tablename__ = "job_descriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    required_skills = Column(JSON)
    min_experience = Column(Integer)
    qualifications = Column(JSON)
    responsibilities = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # Updated
    
    applications = relationship("Application", back_populates="job")

class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    skills = Column(JSON)
    experience = Column(JSON)
    education = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # Updated
    
    applications = relationship("Application", back_populates="candidate")

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("job_descriptions.id"))
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    match_score = Column(Float)
    status = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # Updated
    
    job = relationship("JobDescription", back_populates="applications")
    candidate = relationship("Candidate", back_populates="applications")
    interviews = relationship("Interview", back_populates="application")

class Interview(Base):
    __tablename__ = "interviews"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    scheduled_time = Column(DateTime)
    status = Column(String)
    interview_type = Column(String)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # Updated
    
    application = relationship("Application", back_populates="interviews")

# New User model for authentication
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # Updated