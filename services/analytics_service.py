"""Analytics service for statistics tracking."""
from typing import Dict, Any
from datetime import datetime, timedelta
from loguru import logger
from sqlalchemy.orm import Session

from database.repository import TokenRepository, EventRepository


class AnalyticsService:
    """Service for analytics and statistics."""

    def __init__(self, db_session: Session):
        """Initialize analytics service.

        Args:
            db_session: Database session
        """
        self.token_repo = TokenRepository(db_session)
        self.event_repo = EventRepository(db_session)

    async def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics.

        Returns:
            Statistics dictionary
        """
        try:
            recent_tokens = self.token_repo.get_recent(minutes=1440)  # Last 24 hours
            matched_count = sum(1 for t in recent_tokens if t.matched_filters)
            notified_count = sum(1 for t in recent_tokens if t.notified)

            return {
                "total_tokens_discovered": len(recent_tokens),
                "tokens_matched_filters": matched_count,
                "tokens_notified": notified_count,
                "match_rate_percent": (matched_count / len(recent_tokens) * 100) if recent_tokens else 0,
            }
        except Exception as e:
            logger.error(f"Failed to get summary stats: {e}")
            return {}

    async def get_top_creators(self, limit: int = 10) -> list:
        """Get top token creators.

        Args:
            limit: Maximum results

        Returns:
            List of creators
        """
        try:
            # This would require aggregating by creator
            logger.debug("Getting top creators")
            return []
        except Exception as e:
            logger.error(f"Failed to get top creators: {e}")
            return []
