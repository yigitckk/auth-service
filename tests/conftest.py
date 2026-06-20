import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import get_db
from app.db.database import Base #model importu 
from app.core.security import rate_limit
@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:15-alpine") as postgres:
        db_url = postgres.get_connection_url()
        yield db_url


@pytest.fixture(scope="session")
def db_engine(postgres_container):
    engine = create_engine(postgres_container) #postgres_container url stirng direkt çağırım.
    Base.metadata.create_all(engine)
    yield engine


@pytest.fixture
def db_session(db_engine):
    SessionLocal = sessionmaker(bind=db_engine)
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()   # durign test override data cleaning process.


@pytest.fixture
def client(db_session):
    def override():
        yield db_session
    def override_rate_limit():
        pass 

    app.dependency_overrides[get_db] = override
    app.dependency_overrides[rate_limit] = override_rate_limit
    yield TestClient(app)
    app.dependency_overrides.clear()


