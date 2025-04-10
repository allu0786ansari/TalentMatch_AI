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
    session.query(models.JobDescription).delete()
    session.commit()
    return session

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

def test_create_job(client, test_db):
    """
    Tests creating a job via the API.
    """
    job_data = {
        "title": "Senior Python Developer",
        "required_skills": ["Python", "FastAPI", "SQL"],
        "min_experience": 5,
        "qualifications": ["Bachelor's in Computer Science"],
        "responsibilities": "Develop and maintain backend services"
    }
    
    response = client.post("/api/v1/jobs/", json=job_data)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["title"] == job_data["title"]
    assert set(data["required_skills"]) == set(job_data["required_skills"])

    # Verify job entry in the database
    job = test_db.query(models.JobDescription).filter_by(title=job_data["title"]).first()
    assert job is not None
    assert job.min_experience == job_data["min_experience"]

def test_get_job(client, test_db):
    """
    Tests retrieving a job by ID.
    """
    # Create test job
    job = models.JobDescription(
        title="Test Job",
        required_skills=["Python"],
        min_experience=3,
        qualifications=["Bachelor's"],
        responsibilities="Test responsibilities"
    )
    test_db.add(job)
    test_db.commit()

    response = client.get(f"/api/v1/jobs/{job.id}")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["title"] == "Test Job"
    assert data["min_experience"] == 3