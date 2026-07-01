"""Database connection management."""
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from loguru import logger


class DatabaseConnection:
    """Manages database connections."""

    def __init__(self, database_path: str):
        """Initialize database connection.

        Args:
            database_path: Path to SQLite database file
        """
        self.database_path = database_path
        self.engine = None
        self.SessionLocal = None

    def initialize(self) -> None:
        """Initialize database engine and session factory."""
        try:
            db_dir = Path(self.database_path).parent
            db_dir.mkdir(parents=True, exist_ok=True)

            database_url = f"sqlite:///{self.database_path}"
            self.engine = create_engine(
                database_url,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
            )
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            logger.info(f"Database initialized: {self.database_path}")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    def get_session(self) -> Session:
        """Get new database session.

        Returns:
            Database session
        """
        if self.SessionLocal is None:
            raise RuntimeError("Database not initialized")
        return self.SessionLocal()

    def close(self) -> None:
        """Close database connection."""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")

    def create_tables(self) -> None:
        """Create all tables."""
        try:
            from database.models import Base
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created")
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            raise
