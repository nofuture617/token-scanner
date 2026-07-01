"""Filter validators."""
from typing import Any, Optional
from pydantic import validator, field_validator

from models import FilterConfigModel


class ValidatedFilterConfig(FilterConfigModel):
    """Filter config with validation."""

    @field_validator("min_successful_migrations")
    def validate_migrations(cls, v: int) -> int:
        """Validate minimum successful migrations.

        Args:
            v: Value to validate

        Returns:
            Validated value
        """
        if v < 0:
            raise ValueError("min_successful_migrations must be >= 0")
        return v

    @field_validator("max_created_tokens")
    def validate_max_tokens(cls, v: int) -> int:
        """Validate maximum created tokens.

        Args:
            v: Value to validate

        Returns:
            Validated value
        """
        if v < 1:
            raise ValueError("max_created_tokens must be >= 1")
        return v

    @field_validator("min_success_rate")
    def validate_success_rate(cls, v: float) -> float:
        """Validate minimum success rate.

        Args:
            v: Value to validate

        Returns:
            Validated value
        """
        if not (0 <= v <= 100):
            raise ValueError("min_success_rate must be between 0 and 100")
        return v

    @field_validator("min_liquidity_sol")
    def validate_min_liquidity(cls, v: float) -> float:
        """Validate minimum liquidity.

        Args:
            v: Value to validate

        Returns:
            Validated value
        """
        if v < 0:
            raise ValueError("min_liquidity_sol must be >= 0")
        return v

    @field_validator("min_market_cap_usd", "max_market_cap_usd")
    def validate_market_cap(cls, v: float) -> float:
        """Validate market cap values.

        Args:
            v: Value to validate

        Returns:
            Validated value
        """
        if v < 0:
            raise ValueError("Market cap values must be >= 0")
        return v

    @field_validator("max_dev_ownership_percent")
    def validate_dev_ownership(cls, v: float) -> float:
        """Validate developer ownership percentage.

        Args:
            v: Value to validate

        Returns:
            Validated value
        """
        if not (0 <= v <= 100):
            raise ValueError("max_dev_ownership_percent must be between 0 and 100")
        return v

    @field_validator("max_top_holders_percent")
    def validate_top_holders(cls, v: float) -> float:
        """Validate top holders percentage.

        Args:
            v: Value to validate

        Returns:
            Validated value
        """
        if not (0 <= v <= 100):
            raise ValueError("max_top_holders_percent must be between 0 and 100")
        return v
