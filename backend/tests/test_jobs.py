import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app import models
from app.database import get_db

@pytest.fixture
def test_db(session: Session):
    # Clear existing test data
    session.query(models.JobDescription).delete()
    session.commit()
    return session

@pytest.fixture
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

def test_create_job(client):
    job_data = {
        "title": "Senior Python Developer",
        "required_skills": ["Python", "FastAPI", "SQL"],
        "min_experience": 5,
        "qualifications": ["Bachelor's in Computer Science"],
        "responsibilities": "Develop and maintain backend services"
    }
    
    response = client.post("/api/v1/jobs/", json=job_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == job_data["title"]
    assert set(data["required_skills"]) == set(job_data["required_skills"])

def test_get_job(client, test_db):
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
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Job"