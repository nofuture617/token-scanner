"""Utility validators for data validation."""
from typing import Any, Optional
import re


def is_valid_solana_address(address: str) -> bool:
    """Validate Solana wallet address format.

    Args:
        address: Address to validate

    Returns:
        True if valid, False otherwise
    """
    if not address or not isinstance(address, str):
        return False
    if len(address) < 32 or len(address) > 44:
        return False
    # Basic Solana address validation (base58 characters)
    if not re.match(r"^[1-9A-HJ-NP-Z]{32,44}$", address):
        return False
    return True


def is_valid_percentage(value: Any) -> bool:
    """Validate percentage value (0-100).

    Args:
        value: Value to validate

    Returns:
        True if valid percentage, False otherwise
    """
    try:
        num = float(value)
        return 0 <= num <= 100
    except (TypeError, ValueError):
        return False


def is_valid_token_symbol(symbol: str) -> bool:
    """Validate token symbol format.

    Args:
        symbol: Symbol to validate

    Returns:
        True if valid, False otherwise
    """
    if not symbol or not isinstance(symbol, str):
        return False
    if len(symbol) > 20 or len(symbol) < 1:
        return False
    return symbol.isalnum() or "_" in symbol


def is_valid_mint_address(mint: str) -> bool:
    """Validate mint address (same as Solana address).

    Args:
        mint: Mint address to validate

    Returns:
        True if valid, False otherwise
    """
    return is_valid_solana_address(mint)
