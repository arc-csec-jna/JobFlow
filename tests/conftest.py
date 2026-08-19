import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base

TEST_DATABASE_URL = (
    "postgresql+psycopg://postgres:password@localhost:5432/overseer_test"
)

Testing_sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(TEST_DATABASE_URL))

@pytest.fixture
def db_session():
    # Create the database tables
    Base.metadata.create_all(bind=Testing_sessionLocal().bind)
    session = Testing_sessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=Testing_sessionLocal().bind)
        # Drop the database tables after tests are done