import pytest
from fastapi import UploadFile
from unittest.mock import AsyncMock, MagicMock
from io import BytesIO
import json
from app.utils.resume_parser import parse_resume, Gemini

@pytest.fixture
def mock_pdf_file():
    """
    Provides a mock PDF file with asynchronous behavior for testing.
    """
    file = MagicMock(spec=UploadFile)
    file.filename = "test_resume.pdf"
    file.content_type = "application/pdf"
    
    # Use AsyncMock for the `read` method to simulate asynchronous behavior
    file.read = AsyncMock(return_value=b"%PDF-1.4 Mock PDF content")
    file.file = BytesIO(b"%PDF-1.4 Mock PDF content")  # Simulates a readable file object
    return file

@pytest.fixture
def mock_gemini():
    """
    Provides a mock Gemini instance for testing.
    """
    mock_llm = Gemini(api_key="test_api_key", temperature=0.1, model_name="gemini-1.5-pro")
    mock_llm.run = AsyncMock(return_value=json.dumps({
        "name": "John Doe",
        "email": "john.doe@example.com",
        "skills": ["Python", "FastAPI"],
        "experience": {"Tech Co": 4},
        "education": [{"degree": "BSc Computer Science", "institution": "Test University"}]
    }))
    return mock_llm

@pytest.mark.asyncio
async def test_parse_resume(mock_pdf_file, mock_gemini):
    """
    Tests resume parsing logic using a mock PDF file and mock Gemini instance.
    """
    # Call the parse_resume function with the mock PDF file and mock Gemini instance
    result = await parse_resume(mock_pdf_file, mock_gemini)

    # Assertions
    assert isinstance(result, dict)
    assert "name" in result
    assert "email" in result
    assert "skills" in result
    assert "experience" in result
    assert "education" in result

    assert result["name"] == "John Doe"
    assert result["email"] == "john.doe@example.com"
    assert "Python" in result["skills"]
    assert "Tech Co" in result["experience"]
    assert any("Test University" in edu["institution"] for edu in result["education"])