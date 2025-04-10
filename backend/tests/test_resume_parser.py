import pytest
from fastapi import UploadFile
from app.utils.resume_parser import parse_resume
import io
from unittest.mock import MagicMock

@pytest.fixture
def sample_pdf_content():
    """
    Provides sample resume content mimicking a real resume structure.
    """
    return b"""
    John Doe
    email: john.doe@example.com

    Skills:
    Python, JavaScript, React, SQL

    Experience:
    Tech Corp - Senior Developer (2019-2023)
    CodeCo - Junior Developer (2016-2019)

    Education:
    Masters in Computer Science - Tech University
    Bachelor in IT - Code College
    """

@pytest.fixture
def mock_pdf_file(sample_pdf_content):
    """
    Mocks a PDF file upload.
    """
    file = MagicMock(spec=UploadFile)
    file.filename = "test_resume.pdf"
    file.file = io.BytesIO(sample_pdf_content)  # Simulate file read behavior
    return file

@pytest.mark.asyncio
async def test_parse_resume(mock_pdf_file):
    """
    Tests resume parsing logic using a mock PDF file.
    """
    result = await parse_resume(mock_pdf_file)

    assert isinstance(result, dict)
    assert "name" in result
    assert "email" in result
    assert "skills" in result
    assert "experience" in result
    assert "education" in result

    assert result["name"] == "John Doe"
    assert result["email"] == "john.doe@example.com"
    assert "Python" in result["skills"]
    assert "Tech Corp" in result["experience"]
    assert any("Tech University" in edu["institution"] for edu in result["education"])