import pytest
from fastapi import UploadFile
from app.utils.resume_parser import parse_resume
import io
from unittest.mock import MagicMock

@pytest.fixture
def sample_pdf_content():
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
    file = MagicMock(spec=UploadFile)
    file.filename = "test_resume.pdf"
    file.read = MagicMock(return_value=sample_pdf_content)
    return file

async def test_parse_resume(mock_pdf_file):
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