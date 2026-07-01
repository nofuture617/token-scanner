"""Filter engine for token evaluation."""
from typing import List, Dict, Any
from loguru import logger

from models import TokenModel, FilterConfigModel
from database.repository import DeveloperRepository
from sqlalchemy.orm import Session


class FilterEngine:
    """Evaluates tokens against filter criteria."""

    def __init__(self, session: Session):
        """Initialize filter engine.

        Args:
            session: Database session
        """
        self.session = session
        self.dev_repo = DeveloperRepository(session)

    def evaluate_token(self, token: TokenModel, filters: List[FilterConfigModel]) -> Dict[str, List[str]]:
        """Evaluate token against all enabled filters.

        Args:
            token: Token to evaluate
            filters: List of filter configurations

        Returns:
            Dictionary mapping filter names to match status and reasons
        """
        results = {"matched": [], "not_matched": []}

        for filter_config in filters:
            if not filter_config.enabled:
                continue

            if self._matches_filter(token, filter_config):
                results["matched"].append(filter_config.name)
                logger.info(f"Token {token.symbol} matched filter: {filter_config.name}")
            else:
                results["not_matched"].append(filter_config.name)

        return results

    def _matches_filter(self, token: TokenModel, filter_config: FilterConfigModel) -> bool:
        """Check if token matches all filter criteria.

        Args:
            token: Token to evaluate
            filter_config: Filter configuration

        Returns:
            True if token matches all criteria
        """
        # Check whitelist
        if filter_config.whitelist_addresses:
            if token.creator_address not in filter_config.whitelist_addresses:
                return False

        # Check blacklist
        if filter_config.blacklist_addresses:
            if token.creator_address in filter_config.blacklist_addresses:
                return False

        # Get developer info
        dev = self.dev_repo.get_by_address(token.creator_address)
        if not dev:
            # If developer not in database, use token data
            return self._check_token_criteria(token, filter_config)

        # Check developer whitelisted
        if dev.is_whitelisted:
            return True

        # Check developer blacklisted
        if dev.is_blacklisted:
            return False

        # Check developer metrics
        if dev.successful_launches < filter_config.min_successful_migrations:
            return False

        if dev.total_tokens_created > filter_config.max_created_tokens:
            return False

        if dev.success_rate_percent < filter_config.min_success_rate:
            return False

        return self._check_token_criteria(token, filter_config)

    def _check_token_criteria(self, token: TokenModel, filter_config: FilterConfigModel) -> bool:
        """Check token-specific criteria.

        Args:
            token: Token to check
            filter_config: Filter configuration

        Returns:
            True if token meets criteria
        """
        # Liquidity
        if token.liquidity_sol is not None:
            if token.liquidity_sol < filter_config.min_liquidity_sol:
                return False

        # Market cap
        if token.market_cap_usd is not None:
            if token.market_cap_usd < filter_config.min_market_cap_usd:
                return False
            if token.market_cap_usd > filter_config.max_market_cap_usd:
                return False

        # Holders
        if token.holders_count is not None:
            if token.holders_count < filter_config.min_holders:
                return False

        # Developer ownership
        if token.dev_ownership_percent is not None:
            if token.dev_ownership_percent > filter_config.max_dev_ownership_percent:
                return False

        # Top holders
        if token.top_holders_percent is not None:
            if token.top_holders_percent > filter_config.max_top_holders_percent:
                return False

        # Migration status
        if filter_config.migration_only and not token.is_migrated:
            return False

        # Mint authority
        if filter_config.no_mint_authority and token.has_mint_authority:
            return False

        # Freeze authority
        if filter_config.no_freeze_authority and token.has_freeze_authority:
            return False

        # Liquidity locked
        if filter_config.locked_liquidity_only and not token.liquidity_locked:
            return False

        return True
