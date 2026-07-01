"""Pydantic models for Token data."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class TokenModel(BaseModel):
    """Token data model."""

    mint_address: str = Field(..., description="Token mint address")
    name: str = Field(..., description="Token name")
    symbol: str = Field(..., description="Token symbol")
    creator_address: str = Field(..., description="Token creator wallet")
    price_usd: Optional[float] = Field(None, description="Current price in USD")
    market_cap_usd: Optional[float] = Field(None, description="Market cap in USD")
    fdv_usd: Optional[float] = Field(None, description="Fully diluted valuation in USD")
    volume_usd: Optional[float] = Field(None, description="24h volume in USD")
    liquidity_sol: Optional[float] = Field(None, description="Liquidity in SOL")
    holders_count: Optional[int] = Field(None, description="Number of token holders")
    top_holders_percent: Optional[float] = Field(None, description="Top 10 holders percentage")
    dev_ownership_percent: Optional[float] = Field(None, description="Developer ownership percentage")
    bundle_percent: Optional[float] = Field(None, description="Bundle holder percentage")
    is_migrated: bool = Field(False, description="Token migration status")
    has_mint_authority: bool = Field(True, description="Has mint authority")
    has_freeze_authority: bool = Field(True, description="Has freeze authority")
    liquidity_locked: bool = Field(False, description="Liquidity is locked")
    protocol: Optional[str] = Field(None, description="Creation protocol (e.g., Pump.fun)")
    created_at: datetime = Field(..., description="Token creation time")
    discovered_at: datetime = Field(..., description="When token was discovered")
    axiom_url: Optional[str] = Field(None, description="Axiom Trade page URL")
    twitter_url: Optional[str] = Field(None, description="Twitter profile URL")
    telegram_url: Optional[str] = Field(None, description="Telegram group URL")
    website_url: Optional[str] = Field(None, description="Website URL")

    class Config:
        arbitrary_types_allowed = True


class TokenResponse(TokenModel):
    """Token response from database."""

    id: int = Field(..., description="Database ID")
    matched_filters: List[str] = Field(default_factory=list, description="Matched filter names")
    notified: bool = Field(False, description="User notified")
    browser_opened: bool = Field(False, description="Browser opened for token")
    notes: Optional[str] = Field(None, description="User notes")
