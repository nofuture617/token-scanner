"""Filter service for filter management."""
from typing import List, Optional, Dict, Any
from loguru import logger
from sqlalchemy.orm import Session

from models import FilterConfigModel
from database.repository import FilterConfigRepository


class FilterService:
    """Service for filter operations."""

    def __init__(self, db_session: Session):
        """Initialize filter service.

        Args:
            db_session: Database session
        """
        self.filter_repo = FilterConfigRepository(db_session)

    async def create_filter(self, filter_config: FilterConfigModel) -> bool:
        """Create new filter.

        Args:
            filter_config: Filter configuration

        Returns:
            True if successful
        """
        try:
            self.filter_repo.create(filter_config)
            logger.info(f"Created filter: {filter_config.name}")
            return True
        except Exception as e:
            logger.error(f"Failed to create filter: {e}")
            return False

    async def get_filters(self) -> List[FilterConfigModel]:
        """Get all enabled filters.

        Returns:
            List of filter configurations
        """
        try:
            filters = self.filter_repo.get_enabled()
            return [FilterConfigModel(**{c.name: getattr(f, c.name) for c in f.__table__.columns}) for f in filters]
        except Exception as e:
            logger.error(f"Failed to get filters: {e}")
            return []

    async def get_filter(self, name: str) -> Optional[FilterConfigModel]:
        """Get filter by name.

        Args:
            name: Filter name

        Returns:
            Filter configuration or None
        """
        try:
            filter_orm = self.filter_repo.get_by_name(name)
            if filter_orm:
                return FilterConfigModel(**{c.name: getattr(filter_orm, c.name) for c in filter_orm.__table__.columns})
            return None
        except Exception as e:
            logger.error(f"Failed to get filter: {e}")
            return None

    async def update_filter(self, name: str, filter_config: FilterConfigModel) -> bool:
        """Update filter.

        Args:
            name: Filter name
            filter_config: Updated configuration

        Returns:
            True if successful
        """
        try:
            self.filter_repo.update(name, filter_config)
            logger.info(f"Updated filter: {name}")
            return True
        except Exception as e:
            logger.error(f"Failed to update filter: {e}")
            return False

    async def delete_filter(self, name: str) -> bool:
        """Delete filter.

        Args:
            name: Filter name

        Returns:
            True if successful
        """
        try:
            if self.filter_repo.delete(name):
                logger.info(f"Deleted filter: {name}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete filter: {e}")
            return False
