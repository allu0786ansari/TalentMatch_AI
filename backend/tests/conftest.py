import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
import os

# Create test database engine
TEST_DATABASE_URL = "sqlite:///./tests/test.db"  # Test database path
engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db():
    """
    Ensures that any pre-existing test database is removed before tests run.
    """
    if os.path.exists("./tests/test.db"):
        os.remove("./tests/test.db")

@pytest.fixture(scope="function")
def db_engine():
    """
    Creates and tears down the test database engine for each function test.
    """
    # Create test database tables
    Base.metadata.create_all(bind=engine)
    yield engine
    # Drop test database tables after tests
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def session(db_engine):
    """
    Provides a database session for each test, ensuring transaction rollback
    to maintain test isolation.
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture(scope="session")
def test_job_data():
    """
    Example test data for job endpoints, validated against schemas if necessary.
    """
    return {
        "title": "Senior Python Developer",
        "required_skills": ["Python", "FastAPI", "SQL", "Docker"],
        "min_experience": 5,
        "qualifications": ["Bachelor's in Computer Science", "Master's preferred"],
        "responsibilities": "Lead backend development team and architect solutions"
    }

@pytest.fixture(scope="session")
def test_candidate_data():
    """
    Example test data for candidate endpoints, validated against schemas if necessary.
    """
    return {
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "skills": ["Python", "FastAPI", "SQL", "AWS"],
        "experience": {
            "Tech Corp": "6 years",
            "Dev Inc": "3 years"
        },
        "education": [
            {
                "degree": "Master of Computer Science",
                "institution": "Tech University"
            },
            {
                "degree": "Bachelor of Engineering",
                "institution": "Engineering College"
            }
        ]
    }

@pytest.fixture(scope="session")
def test_interview_data():
    """
    Example test data for interview endpoints, validated against schemas if necessary.
    """
    return {
        "interview_type": "technical",
        "scheduled_time": "2024-04-15T10:00:00",
        "notes": "Focus on system design and coding skills"
    }