"""Pydantic models for Developer data."""
from typing import Optional
from pydantic import BaseModel, Field


class DeveloperModel(BaseModel):
    """Developer data model."""

    address: str = Field(..., description="Developer wallet address")
    total_tokens_created: int = Field(0, description="Total tokens created")
    successful_launches: int = Field(0, description="Number of successful launches")
    success_rate_percent: float = Field(0.0, description="Success rate percentage")
    migrated_tokens: int = Field(0, description="Tokens that migrated")
    last_token_created: Optional[str] = Field(None, description="Most recent token mint")
    is_blacklisted: bool = Field(False, description="Developer blacklisted")
    is_whitelisted: bool = Field(False, description="Developer whitelisted")
    notes: Optional[str] = Field(None, description="Notes about developer")

    class Config:
        arbitrary_types_allowed = True
