"""API response handlers."""
from typing import Dict, Any, Optional
from datetime import datetime
from loguru import logger

from models import TokenModel
from utils import safe_get, parse_json_safe


class TokenResponseHandler:
    """Handles token data from API."""

    @staticmethod
    def parse_token(data: Dict[str, Any]) -> Optional[TokenModel]:
        """Parse token data from API response.

        Args:
            data: Raw token data from API

        Returns:
            TokenModel or None if parsing fails
        """
        try:
            mint = safe_get(data, "mint", "address", "tokenMint")
            if not mint:
                logger.warning("Missing mint address in token data")
                return None

            token = TokenModel(
                mint_address=mint,
                name=safe_get(data, "name", "tokenName", default="Unknown"),
                symbol=safe_get(data, "symbol", "ticker", default=""),
                creator_address=safe_get(data, "creator", "deployer", "creatorAddress", default=""),
                price_usd=safe_get(data, "price", "priceUsd", default=None),
                market_cap_usd=safe_get(data, "marketCap", "marketCapSol", "marketCapUsd", default=None),
                fdv_usd=safe_get(data, "fdv", "fullyDilutedValuation", default=None),
                volume_usd=safe_get(data, "volume", "volume24h", "volumeUsd", default=None),
                liquidity_sol=safe_get(data, "liquidity", "liquiditySol", default=None),
                holders_count=safe_get(data, "holders", "holdersCount", default=None),
                top_holders_percent=safe_get(data, "topHolders", "topHoldersPercent", default=None),
                dev_ownership_percent=safe_get(data, "devOwnership", "devOwnershipPercent", default=None),
                bundle_percent=safe_get(data, "bundle", "bundlePercent", default=None),
                is_migrated=safe_get(data, "isMigrated", "migrated", default=False),
                has_mint_authority=safe_get(data, "hasMintAuthority", "mintAuthority", default=True),
                has_freeze_authority=safe_get(data, "hasFreezeAuthority", "freezeAuthority", default=True),
                liquidity_locked=safe_get(data, "liquidityLocked", "locked", default=False),
                protocol=safe_get(data, "protocol", "platform", default=None),
                created_at=TokenResponseHandler._parse_datetime(safe_get(data, "createdAt", "created_at")),
                discovered_at=datetime.utcnow(),
                axiom_url=TokenResponseHandler._build_axiom_url(mint),
                twitter_url=safe_get(data, "twitter", "twitterUrl", default=None),
                telegram_url=safe_get(data, "telegram", "telegramUrl", default=None),
                website_url=safe_get(data, "website", "websiteUrl", default=None),
            )
            return token
        except Exception as e:
            logger.error(f"Failed to parse token data: {e}")
            return None

    @staticmethod
    def _parse_datetime(value: Any) -> datetime:
        """Parse datetime from various formats.

        Args:
            value: Datetime value

        Returns:
            Parsed datetime or current UTC time
        """
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                pass
        return datetime.utcnow()

    @staticmethod
    def _build_axiom_url(mint_address: str) -> str:
        """Build Axiom Trade URL for token.

        Args:
            mint_address: Token mint address

        Returns:
            Axiom Trade URL
        """
        return f"https://axiom.trade/token/{mint_address}"
