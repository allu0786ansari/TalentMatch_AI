import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from backend.app.main import app
from backend.app import models
from backend.app.database import get_db

@pytest.fixture
def test_db(session: Session):
    session.query(models.Candidate).delete()
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

def test_create_candidate(client):
    candidate_data = {
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "skills": ["Python", "React", "SQL"],
        "experience": {
            "Company A": "3 years",
            "Company B": "2 years"
        },
        "education": [
            {
                "degree": "Masters in Computer Science",
                "institution": "Tech University"
            }
        ]
    }
    
    response = client.post("/api/v1/candidates/", json=candidate_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == candidate_data["name"]
    assert data["email"] == candidate_data["email"]

@pytest.mark.asyncio
async def test_upload_resume(client, mock_pdf_file):
    files = {"file": ("test_resume.pdf", mock_pdf_file, "application/pdf")}
    response = client.post("/api/v1/candidates/upload-resume", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "email" in data