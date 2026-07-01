"""Helper functions for common operations."""
from datetime import datetime, timezone
from typing import Any, Dict, Optional, List
import json


def get_now_utc() -> datetime:
    """Get current UTC datetime.

    Returns:
        Current datetime in UTC timezone
    """
    return datetime.now(timezone.utc)


def safe_get(data: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    """Safely get nested dictionary value.

    Args:
        data: Dictionary to search
        *keys: Keys to traverse
        default: Default value if not found

    Returns:
        Value or default
    """
    current = data
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
            if current is None:
                return default
        else:
            return default
    return current if current is not None else default


def parse_json_safe(data: str, default: Any = None) -> Any:
    """Safely parse JSON string.

    Args:
        data: JSON string
        default: Default value if parsing fails

    Returns:
        Parsed data or default
    """
    try:
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return default


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate string to max length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def chunk_list(items: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split list into chunks.

    Args:
        items: List to chunk
        chunk_size: Size of each chunk

    Returns:
        List of chunks
    """
    return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]


def retry_async(max_attempts: int = 3, delay: float = 1.0):
    """Decorator for async function retry logic.

    Args:
        max_attempts: Maximum retry attempts
        delay: Delay between attempts in seconds

    Returns:
        Decorator function
    """
    import asyncio
    from functools import wraps

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        await asyncio.sleep(delay * (2 ** attempt))
            raise last_exception

        return wrapper

    return decorator
