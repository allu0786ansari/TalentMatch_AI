import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app
from app import models
from app.database import get_db
from http import HTTPStatus

@pytest.fixture(scope="function")
def test_db(session: Session):
    """
    Provides a clean database session for each test.
    """
    session.query(models.Application).delete()
    session.query(models.JobDescription).delete()
    session.query(models.Candidate).delete()
    session.commit()
    return session

@pytest.fixture
def test_job(test_db):
    """
    Creates a mock job entry for testing.
    """
    job = models.JobDescription(
        title="Python Developer",
        required_skills=["Python", "FastAPI", "SQL"],
        min_experience=3,
        qualifications=["Bachelor's in Computer Science"],
        responsibilities="Backend development"
    )
    test_db.add(job)
    test_db.commit()
    return job

@pytest.fixture
def test_candidate(test_db):
    """
    Creates a mock candidate entry for testing.
    """
    candidate = models.Candidate(
        name="Test Developer",
        email="test@example.com",
        skills=["Python", "FastAPI", "MongoDB"],
        experience={"Tech Co": "4 years"},
        education=[{"degree": "BSc Computer Science", "institution": "Test University"}]
    )
    test_db.add(candidate)
    test_db.commit()
    return candidate

@pytest.fixture
def client(test_db):
    """
    Provides a FastAPI TestClient with database override.
    """
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

def test_match_candidates(client, test_job, test_candidate):
    """
    Tests matching candidates to a job.
    """
    response = client.post(f"/api/v1/matches/match/{test_job.id}")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["job_id"] == test_job.id
    assert data[0]["candidate_id"] == test_candidate.id
    assert "match_score" in data[0]
    assert data[0]["status"] in ["pending", "shortlisted"]

def test_get_job_applications(client, test_job, test_candidate, test_db):
    """
    Tests retrieving applications for a job.
    """
    # Create a test application
    application = models.Application(
        job_id=test_job.id,
        candidate_id=test_candidate.id,
        match_score=0.85,
        status="shortlisted"
    )
    test_db.add(application)
    test_db.commit()

    # Verify the application exists in the database before calling API
    stored_application = test_db.query(models.Application).filter_by(job_id=test_job.id).first()
    assert stored_application is not None
    assert stored_application.match_score == 0.85

    response = client.get(f"/api/v1/matches/applications/{test_job.id}")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["job_id"] == test_job.id
    assert data[0]["match_score"] == 0.85