"""Repository pattern for data access."""
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from loguru import logger
import json

from database.models import TokenORM, DeveloperORM, FilterConfigORM, EventORM
from models import TokenModel, DeveloperModel, FilterConfigModel, EventModel, EventType


class TokenRepository:
    """Token data repository."""

    def __init__(self, session: Session):
        """Initialize repository.

        Args:
            session: Database session
        """
        self.session = session

    def create_or_update(self, token_data: TokenModel) -> TokenORM:
        """Create or update token.

        Args:
            token_data: Token data model

        Returns:
            Token ORM object
        """
        try:
            existing = self.session.query(TokenORM).filter_by(mint_address=token_data.mint_address).first()
            
            if existing:
                for key, value in token_data.dict(exclude_unset=True).items():
                    setattr(existing, key, value)
                self.session.add(existing)
                logger.debug(f"Updated token: {token_data.symbol}")
                return existing
            else:
                token_orm = TokenORM(**token_data.dict())
                self.session.add(token_orm)
                logger.debug(f"Created token: {token_data.symbol}")
                return token_orm
        finally:
            self.session.commit()

    def get_by_mint(self, mint_address: str) -> Optional[TokenORM]:
        """Get token by mint address.

        Args:
            mint_address: Token mint address

        Returns:
            Token ORM object or None
        """
        return self.session.query(TokenORM).filter_by(mint_address=mint_address).first()

    def get_all(self, limit: int = 100, offset: int = 0) -> List[TokenORM]:
        """Get all tokens with pagination.

        Args:
            limit: Maximum results
            offset: Results offset

        Returns:
            List of token ORM objects
        """
        return self.session.query(TokenORM).order_by(desc(TokenORM.discovered_at)).limit(limit).offset(offset).all()

    def get_recent(self, minutes: int = 60) -> List[TokenORM]:
        """Get recently discovered tokens.

        Args:
            minutes: Minutes back to search

        Returns:
            List of token ORM objects
        """
        cutoff = datetime.utcnow() - timedelta(minutes=minutes)
        return self.session.query(TokenORM).filter(TokenORM.discovered_at >= cutoff).order_by(desc(TokenORM.discovered_at)).all()

    def get_by_creator(self, creator_address: str) -> List[TokenORM]:
        """Get tokens by creator address.

        Args:
            creator_address: Creator wallet address

        Returns:
            List of token ORM objects
        """
        return self.session.query(TokenORM).filter_by(creator_address=creator_address).all()

    def update_matched_filters(self, mint_address: str, filter_names: List[str]) -> None:
        """Update matched filters for token.

        Args:
            mint_address: Token mint address
            filter_names: List of matched filter names
        """
        token = self.get_by_mint(mint_address)
        if token:
            token.matched_filters = json.dumps(filter_names)
            self.session.commit()

    def mark_notified(self, mint_address: str) -> None:
        """Mark token as notified.

        Args:
            mint_address: Token mint address
        """
        token = self.get_by_mint(mint_address)
        if token:
            token.notified = True
            self.session.commit()

    def mark_browser_opened(self, mint_address: str) -> None:
        """Mark token as browser opened.

        Args:
            mint_address: Token mint address
        """
        token = self.get_by_mint(mint_address)
        if token:
            token.browser_opened = True
            self.session.commit()

    def delete_old_tokens(self, days: int = 30) -> int:
        """Delete old token records.

        Args:
            days: Delete tokens older than this many days

        Returns:
            Number of deleted records
        """
        cutoff = datetime.utcnow() - timedelta(days=days)
        count = self.session.query(TokenORM).filter(TokenORM.discovered_at < cutoff).delete()
        self.session.commit()
        return count


class DeveloperRepository:
    """Developer data repository."""

    def __init__(self, session: Session):
        """Initialize repository.

        Args:
            session: Database session
        """
        self.session = session

    def create_or_update(self, dev_data: DeveloperModel) -> DeveloperORM:
        """Create or update developer.

        Args:
            dev_data: Developer data model

        Returns:
            Developer ORM object
        """
        try:
            existing = self.session.query(DeveloperORM).filter_by(address=dev_data.address).first()
            
            if existing:
                for key, value in dev_data.dict(exclude_unset=True).items():
                    setattr(existing, key, value)
                self.session.add(existing)
                return existing
            else:
                dev_orm = DeveloperORM(**dev_data.dict())
                self.session.add(dev_orm)
                return dev_orm
        finally:
            self.session.commit()

    def get_by_address(self, address: str) -> Optional[DeveloperORM]:
        """Get developer by address.

        Args:
            address: Developer wallet address

        Returns:
            Developer ORM object or None
        """
        return self.session.query(DeveloperORM).filter_by(address=address).first()

    def is_whitelisted(self, address: str) -> bool:
        """Check if developer is whitelisted.

        Args:
            address: Developer address

        Returns:
            True if whitelisted
        """
        dev = self.get_by_address(address)
        return dev and dev.is_whitelisted if dev else False

    def is_blacklisted(self, address: str) -> bool:
        """Check if developer is blacklisted.

        Args:
            address: Developer address

        Returns:
            True if blacklisted
        """
        dev = self.get_by_address(address)
        return dev and dev.is_blacklisted if dev else False


class FilterConfigRepository:
    """Filter configuration repository."""

    def __init__(self, session: Session):
        """Initialize repository.

        Args:
            session: Database session
        """
        self.session = session

    def create(self, filter_data: FilterConfigModel) -> FilterConfigORM:
        """Create new filter.

        Args:
            filter_data: Filter configuration model

        Returns:
            Filter config ORM object
        """
        try:
            filter_orm = FilterConfigORM(
                **filter_data.dict(
                    exclude={"whitelist_addresses", "blacklist_addresses"}
                ),
                whitelist_addresses=json.dumps(filter_data.whitelist_addresses),
                blacklist_addresses=json.dumps(filter_data.blacklist_addresses),
            )
            self.session.add(filter_orm)
            self.session.commit()
            logger.info(f"Created filter: {filter_data.name}")
            return filter_orm
        except Exception as e:
            logger.error(f"Failed to create filter: {e}")
            self.session.rollback()
            raise

    def get_by_name(self, name: str) -> Optional[FilterConfigORM]:
        """Get filter by name.

        Args:
            name: Filter name

        Returns:
            Filter config ORM object or None
        """
        return self.session.query(FilterConfigORM).filter_by(name=name).first()

    def get_enabled(self) -> List[FilterConfigORM]:
        """Get all enabled filters.

        Returns:
            List of enabled filter configs
        """
        return self.session.query(FilterConfigORM).filter_by(enabled=True).order_by(desc(FilterConfigORM.priority)).all()

    def update(self, name: str, filter_data: FilterConfigModel) -> Optional[FilterConfigORM]:
        """Update filter.

        Args:
            name: Filter name
            filter_data: Updated filter data

        Returns:
            Updated filter config or None
        """
        try:
            existing = self.get_by_name(name)
            if not existing:
                return None
            
            for key, value in filter_data.dict().items():
                if key in ["whitelist_addresses", "blacklist_addresses"]:
                    setattr(existing, key, json.dumps(value))
                else:
                    setattr(existing, key, value)
            
            self.session.commit()
            logger.info(f"Updated filter: {name}")
            return existing
        except Exception as e:
            logger.error(f"Failed to update filter: {e}")
            self.session.rollback()
            raise

    def delete(self, name: str) -> bool:
        """Delete filter.

        Args:
            name: Filter name

        Returns:
            True if deleted
        """
        try:
            existing = self.get_by_name(name)
            if not existing:
                return False
            
            self.session.delete(existing)
            self.session.commit()
            logger.info(f"Deleted filter: {name}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete filter: {e}")
            self.session.rollback()
            raise


class EventRepository:
    """Event log repository."""

    def __init__(self, session: Session):
        """Initialize repository.

        Args:
            session: Database session
        """
        self.session = session

    def create(self, event_data: EventModel) -> EventORM:
        """Create new event.

        Args:
            event_data: Event data model

        Returns:
            Event ORM object
        """
        try:
            event_orm = EventORM(
                **event_data.dict(exclude={"data"}),
                data=json.dumps(event_data.data)
            )
            self.session.add(event_orm)
            self.session.commit()
            return event_orm
        except Exception as e:
            logger.error(f"Failed to create event: {e}")
            self.session.rollback()
            raise

    def get_recent(self, limit: int = 100, event_type: Optional[str] = None) -> List[EventORM]:
        """Get recent events.

        Args:
            limit: Maximum results
            event_type: Filter by event type

        Returns:
            List of event ORM objects
        """
        query = self.session.query(EventORM).order_by(desc(EventORM.timestamp))
        if event_type:
            query = query.filter_by(type=event_type)
        return query.limit(limit).all()

    def delete_old_events(self, days: int = 30) -> int:
        """Delete old events.

        Args:
            days: Delete events older than this many days

        Returns:
            Number of deleted records
        """
        cutoff = datetime.utcnow() - timedelta(days=days)
        count = self.session.query(EventORM).filter(EventORM.timestamp < cutoff).delete()
        self.session.commit()
        return count
