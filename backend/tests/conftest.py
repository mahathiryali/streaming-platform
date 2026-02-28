import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Use an in-memory database for even faster tests, 
# or keep the file-based one as you had it:
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create the database structure once per test session."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    """Yields a fresh session for every test and rolls back after."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    """Overrides get_db with the test session and yields the TestClient."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass # Session is closed by the db_session fixture

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    # Clear overrides after the test is done
    app.dependency_overrides.clear()

@pytest.fixture
def test_user():
    return {"email": "test@example.com", "password": "password123"}

@pytest.fixture
def registered_user(client, test_user):
    """Fixture to ensure a user exists before a test runs."""
    response = client.post("/auth/register", json=test_user)
    return response.json()