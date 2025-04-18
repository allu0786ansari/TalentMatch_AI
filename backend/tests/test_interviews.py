import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from main import app
from app import models
from app.database import get_db
from http import HTTPStatus

@pytest.fixture(scope="function")
def test_db(session: Session):
    """
    Provides a clean test database session.
    """
    session.query(models.Interview).delete()
    session.query(models.Application).delete()
    session.commit()
    return session

@pytest.fixture
def test_job(test_db):
    """
    Mock job entry for testing.
    """
    job = models.JobDescription(
        title="Software Developer",
        required_skills=["Python", "SQL", "FastAPI"],
        min_experience=3
    )
    test_db.add(job)
    test_db.commit()
    return job

@pytest.fixture
def test_candidate(test_db):
    """
    Mock candidate entry for testing.
    """
    candidate = models.Candidate(
        name="John Doe",
        email="john.doe@example.com",
        skills=["Python", "SQL"],
        experience={"Company": "3 years"}
    )
    test_db.add(candidate)
    test_db.commit()
    return candidate

@pytest.fixture
def test_application(test_db, test_job, test_candidate):
    """
    Mock application entry for testing interviews.
    """
    application = models.Application(
        job_id=test_job.id,
        candidate_id=test_candidate.id,
        match_score=0.9,
        status="shortlisted"
    )
    test_db.add(application)
    test_db.commit()
    return application

@pytest.fixture
def client(test_db):
    """
    Provides a FastAPI TestClient with a test database override.
    """
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

def test_schedule_interview(client, test_application):
    """
    Tests scheduling an interview.
    """
    interview_data = {
        "application_id": test_application.id,
        "scheduled_time": (datetime.now(tz=timezone.utc) + timedelta(days=2)).isoformat(),
        "interview_type": "video",
        "notes": "Technical interview round"
    }
    
    response = client.post("/api/v1/interviews/schedule", json=interview_data)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["application_id"] == test_application.id
    assert data["interview_type"] == "video"
    assert data["status"] == "scheduled"

def test_get_interview(client, test_application, test_db):
    """
    Tests fetching an interview by application ID.
    """
    # Create test interview
    interview = models.Interview(
        application_id=test_application.id,
        scheduled_time=datetime.now(tz=timezone.utc) + timedelta(days=1),
        status="scheduled",
        interview_type="video"
    )
    test_db.add(interview)
    test_db.commit()
    
    # Fetch the interview via API
    response = client.get(f"/api/v1/interviews/{test_application.id}")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["application_id"] == test_application.id
    assert data["status"] == "scheduled"