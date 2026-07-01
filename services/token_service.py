"""Token service for token processing."""
from typing import Optional, List, Dict, Any
from loguru import logger
from sqlalchemy.orm import Session

from models import TokenModel
from database.repository import TokenRepository, DeveloperRepository


class TokenService:
    """Service for token operations."""

    def __init__(self, db_session: Session):
        """Initialize token service.

        Args:
            db_session: Database session
        """
        self.token_repo = TokenRepository(db_session)
        self.dev_repo = DeveloperRepository(db_session)

    async def process_token(self, token: TokenModel) -> bool:
        """Process and store token.

        Args:
            token: Token model

        Returns:
            True if successful
        """
        try:
            self.token_repo.create_or_update(token)
            logger.info(f"Processed token: {token.symbol}")
            return True
        except Exception as e:
            logger.error(f"Failed to process token: {e}")
            return False

    async def get_token(self, mint_address: str) -> Optional[TokenModel]:
        """Get token by mint address.

        Args:
            mint_address: Token mint address

        Returns:
            Token model or None
        """
        try:
            token_orm = self.token_repo.get_by_mint(mint_address)
            if token_orm:
                return TokenModel(**{c.name: getattr(token_orm, c.name) for c in token_orm.__table__.columns})
            return None
        except Exception as e:
            logger.error(f"Failed to get token: {e}")
            return None

    async def get_recent_tokens(self, minutes: int = 60, limit: int = 100) -> List[TokenModel]:
        """Get recently discovered tokens.

        Args:
            minutes: Minutes back to search
            limit: Maximum results

        Returns:
            List of token models
        """
        try:
            tokens = self.token_repo.get_recent(minutes=minutes)
            return tokens[:limit]
        except Exception as e:
            logger.error(f"Failed to get recent tokens: {e}")
            return []
