"""Pydantic models for filter configuration."""
from typing import Optional, List
from pydantic import BaseModel, Field


class FilterConfigModel(BaseModel):
    """Filter configuration model."""

    name: str = Field(..., description="Filter name")
    enabled: bool = Field(True, description="Filter is enabled")
    
    # Developer metrics
    min_successful_migrations: int = Field(1, description="Minimum successful migrations")
    max_created_tokens: int = Field(100, description="Maximum tokens created")
    min_success_rate: float = Field(0.0, description="Minimum success rate %")
    
    # Liquidity and pricing
    min_liquidity_sol: float = Field(2.0, description="Minimum liquidity in SOL")
    min_market_cap_usd: float = Field(0, description="Minimum market cap USD")
    max_market_cap_usd: float = Field(10_000_000, description="Maximum market cap USD")
    
    # Distribution
    min_holders: int = Field(10, description="Minimum holders count")
    max_dev_ownership_percent: float = Field(50.0, description="Maximum dev ownership %")
    max_top_holders_percent: float = Field(100.0, description="Maximum top 10 holders %")
    
    # Status filters
    migration_only: bool = Field(False, description="Only migrated tokens")
    no_mint_authority: bool = Field(False, description="No mint authority")
    no_freeze_authority: bool = Field(False, description="No freeze authority")
    locked_liquidity_only: bool = Field(False, description="Only locked liquidity")
    
    # Lists
    whitelist_addresses: List[str] = Field(default_factory=list, description="Whitelist")
    blacklist_addresses: List[str] = Field(default_factory=list, description="Blacklist")
    
    # Notifications
    send_notification: bool = Field(True, description="Send notification on match")
    auto_open_browser: bool = Field(True, description="Auto open browser")
    
    # Metadata
    description: Optional[str] = Field(None, description="Filter description")
    priority: int = Field(0, description="Filter priority (higher = more important)")

    class Config:
        arbitrary_types_allowed = True
