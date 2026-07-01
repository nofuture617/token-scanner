"""Utility functions for logging setup."""
import sys
from pathlib import Path
from loguru import logger


def setup_logger(debug: bool = False, log_level: str = "INFO") -> None:
    """Configure loguru logger.

    Args:
        debug: Enable debug mode
        log_level: Logging level
    """
    # Remove default handler
    logger.remove()

    # Console handler
    level = "DEBUG" if debug else log_level
    logger.add(
        sys.stderr,
        format="<level>{time:YYYY-MM-DD HH:mm:ss}</level> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=level,
        colorize=True,
    )

    # File handler
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    logger.add(
        logs_dir / "scanner.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="500 MB",
        retention="30 days",
        compression="zip",
    )

    # WebSocket events
    logger.add(
        logs_dir / "websocket.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        level="DEBUG",
        rotation="100 MB",
        retention="7 days",
    )

    logger.info(f"Logger initialized | Debug: {debug} | Level: {level}")


if __name__ == "__main__":
    setup_logger(debug=True)
    logger.debug("Test debug message")
    logger.info("Test info message")
    logger.warning("Test warning message")
    logger.error("Test error message")
