import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.main import app
from app import models
from app.database import get_db

@pytest.fixture
def test_db(session: Session):
    # Clean up existing test data
    session.query(models.Interview).delete()
    session.query(models.Application).delete()
    session.commit()
    return session

@pytest.fixture
def test_application(test_db, test_job, test_candidate):
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
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

def test_schedule_interview(client, test_application):
    interview_data = {
        "application_id": test_application.id,
        "scheduled_time": (datetime.now() + timedelta(days=2)).isoformat(),
        "interview_type": "video",
        "notes": "Technical interview round"
    }
    
    response = client.post("/api/v1/interviews/schedule", json=interview_data)
    assert response.status_code == 200
    data = response.json()
    assert data["application_id"] == test_application.id
    assert data["interview_type"] == "video"
    assert data["status"] == "scheduled"

def test_get_interview(client, test_application):
    # Create test interview
    interview = models.Interview(
        application_id=test_application.id,
        scheduled_time=datetime.now() + timedelta(days=1),
        status="scheduled",
        interview_type="video"
    )
    test_db = next(get_db())
    test_db.add(interview)
    test_db.commit()

    response = client.get(f"/api/v1/interviews/{test_application.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["application_id"] == test_application.id
    assert data["status"] == "scheduled"