import pytest
from fastapi import UploadFile
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app
from app import models
from app.database import get_db
from io import BytesIO

@pytest.fixture
def test_db(session: Session):
    """
    Prepares a clean test database session.
    """
    session.query(models.Candidate).delete()  # Clear the table
    session.commit()
    return session

@pytest.fixture
def mock_pdf_file():
    """
    Provides a mock PDF file for testing.
    """
    file_content = b"%PDF-1.4 mock PDF content"
    return UploadFile(filename="mock_resume.pdf", file=BytesIO(file_content))

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

def test_create_candidate(client, test_db):
    """
    Tests the creation of a candidate via the API.
    """
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

    # Verify the candidate exists in the database
    candidate = test_db.query(models.Candidate).filter(models.Candidate.email == candidate_data["email"]).first()
    assert candidate is not None
    assert candidate.name == candidate_data["name"]

def test_upload_resume(client, mock_pdf_file):
    """
    Tests the upload of a resume via the API.
    """
    files = {"file": ("test_resume.pdf", mock_pdf_file, "application/pdf")}
    response = client.post("/api/v1/candidates/upload-resume", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "email" in data