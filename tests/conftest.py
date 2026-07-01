"""Test configuration and fixtures."""
import pytest
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import tempfile

from database import DatabaseConnection, Base


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_db():
    """Create temporary database for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        
        db_conn = DatabaseConnection(str(db_path))
        db_conn.initialize()
        db_conn.create_tables()
        
        yield db_conn
        
        db_conn.close()
