"""
Pytest Configuration and Fixtures

This file contains shared fixtures and configuration for all tests.
"""

import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.models.user import User
from app.models.dataset import Dataset
from app.core.security import get_password_hash, create_access_token

# Test database URL (in-memory SQLite)
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

# Create test engine
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False  # Set to True for SQL debugging
)

# Create test session (synchronous for SQLite testing)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture(scope="function")
def db_session():
    """
    Create a fresh database for each test.
    """
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Create a test client with database session override.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """
    Create a test user in the database.
    """
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("testpassword123"),
        full_name="Test User",
        is_active=True,
        is_superuser=False
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_superuser(db_session):
    """
    Create a test superuser in the database.
    """
    user = User(
        email="admin@example.com",
        username="admin",
        hashed_password=get_password_hash("adminpassword123"),
        full_name="Admin User",
        is_active=True,
        is_superuser=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_token(test_user):
    """
    Create an authentication token for the test user.
    """
    token = create_access_token(data={"sub": test_user.email})
    return token


@pytest.fixture
def auth_headers(auth_token):
    """
    Create authorization headers with the test token.
    """
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def test_dataset(db_session, test_user):
    """
    Create a test dataset in the database.
    """
    dataset = Dataset(
        user_id=test_user.id,
        filename="test_dataset.csv",
        original_filename="test_data.csv",
        file_type="csv",
        file_size=1024,
        file_path="uploads/test_dataset.csv",
        row_count=100,
        column_count=5,
        columns_info={"columns": ["col1", "col2", "col3", "col4", "col5"]},
        status="ready"  # Changed from "completed" to match DatasetStatus enum
    )
    db_session.add(dataset)
    db_session.commit()
    db_session.refresh(dataset)
    return dataset


@pytest.fixture
def sample_csv_file():
    """
    Create a sample CSV file for upload testing.
    """
    import io
    csv_content = """name,age,city,salary,department
John Doe,30,New York,75000,Engineering
Jane Smith,25,San Francisco,85000,Marketing
Bob Johnson,35,Chicago,65000,Sales
Alice Williams,28,Boston,70000,Engineering
Charlie Brown,32,Seattle,80000,Marketing"""
    
    return io.BytesIO(csv_content.encode())


@pytest.fixture
def sample_csv_file_with_errors():
    """
    Create a CSV file with data quality issues for testing error handling.
    """
    import io
    csv_content = """name,age,city,salary
John Doe,30,New York,75000
Jane Smith,invalid_age,San Francisco,85000
Bob Johnson,35,,65000
,28,Boston,70000"""
    
    return io.BytesIO(csv_content.encode())


@pytest.fixture(autouse=True)
def cleanup_uploads():
    """
    Clean up uploaded files after each test.
    """
    yield
    
    # Cleanup logic here if needed
    upload_dir = "uploads"
    if os.path.exists(upload_dir):
        for file in os.listdir(upload_dir):
            if file != ".gitkeep":
                file_path = os.path.join(upload_dir, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")


# Test configuration
def pytest_configure(config):
    """
    Configure pytest with custom markers.
    """
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
