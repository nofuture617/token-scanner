"""Utility formatters for data formatting."""
from datetime import datetime, timezone
from typing import Optional


def format_price(price: float) -> str:
    """Format price for display.

    Args:
        price: Price value

    Returns:
        Formatted price string
    """
    if price == 0:
        return "$0.00"
    if price < 0.00001:
        return f"${price:.2e}"
    if price < 1:
        return f"${price:.6f}"
    return f"${price:,.2f}"


def format_market_cap(market_cap: float) -> str:
    """Format market cap for display.

    Args:
        market_cap: Market cap value in USD

    Returns:
        Formatted market cap string
    """
    if market_cap == 0:
        return "$0"
    if market_cap >= 1_000_000:
        return f"${market_cap / 1_000_000:.2f}M"
    if market_cap >= 1_000:
        return f"${market_cap / 1_000:.2f}K"
    return f"${market_cap:,.2f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """Format percentage for display.

    Args:
        value: Percentage value (0-100)
        decimals: Number of decimal places

    Returns:
        Formatted percentage string
    """
    return f"{value:.{decimals}f}%"


def format_token_age(created_at: datetime) -> str:
    """Format token age as human-readable string.

    Args:
        created_at: Token creation datetime

    Returns:
        Formatted age string (e.g., "5m", "2h", "1d")
    """
    now = datetime.now(timezone.utc)
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)

    age_seconds = (now - created_at).total_seconds()

    if age_seconds < 60:
        return f"{int(age_seconds)}s"
    if age_seconds < 3600:
        return f"{int(age_seconds / 60)}m"
    if age_seconds < 86400:
        return f"{int(age_seconds / 3600)}h"
    return f"{int(age_seconds / 86400)}d"


def format_address_short(address: str, chars: int = 6) -> str:
    """Format wallet address in short form.

    Args:
        address: Full wallet address
        chars: Number of characters to show at start and end

    Returns:
        Shortened address (e.g., "ABC...XYZ")
    """
    if len(address) <= chars * 2 + 3:
        return address
    return f"{address[:chars]}...{address[-chars:]}"


def format_volume(volume: float) -> str:
    """Format trading volume for display.

    Args:
        volume: Volume value in USD or SOL

    Returns:
        Formatted volume string
    """
    if volume == 0:
        return "$0"
    if volume >= 1_000_000:
        return f"${volume / 1_000_000:.2f}M"
    if volume >= 1_000:
        return f"${volume / 1_000:.2f}K"
    return f"${volume:,.2f}"
