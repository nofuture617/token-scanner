"""Scanner stream handler for WebSocket data."""
from typing import Callable, Dict, Any
from loguru import logger
import asyncio

from models import TokenModel
from api.handlers import TokenResponseHandler


class WebSocketStream:
    """Handles WebSocket stream for new tokens."""

    def __init__(self, on_token_received: Callable):
        """Initialize WebSocket stream handler.

        Args:
            on_token_received: Callback function when token received
        """
        self.on_token_received = on_token_received
        self.is_connected = False
        self.token_count = 0

    async def handle_message(self, data: Dict[str, Any]) -> None:
        """Handle incoming WebSocket message.

        Args:
            data: Message data from WebSocket
        """
        try:
            # Parse token from message
            token_data = self._extract_token_data(data)
            if not token_data:
                logger.warning("Failed to extract token data from message")
                return

            # Parse into TokenModel
            token = TokenResponseHandler.parse_token(token_data)
            if not token:
                logger.warning("Failed to parse token")
                return

            self.token_count += 1
            logger.debug(f"Received token: {token.symbol} (Total: {self.token_count})")

            # Call callback
            await self.on_token_received(token)
        except Exception as e:
            logger.error(f"Error handling WebSocket message: {e}")

    def _extract_token_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract token data from WebSocket message.

        Args:
            data: Raw message data

        Returns:
            Token data dictionary or None
        """
        if isinstance(data, dict):
            # Try different message formats
            if "content" in data:
                return data["content"]
            if "token" in data:
                return data["token"]
            return data
        return None

    def set_connected(self, connected: bool) -> None:
        """Set connection status.

        Args:
            connected: Connection status
        """
        self.is_connected = connected
        status = "connected" if connected else "disconnected"
        logger.info(f"WebSocket stream {status}")

    def get_stats(self) -> Dict[str, Any]:
        """Get stream statistics.

        Returns:
            Statistics dictionary
        """
        return {
            "is_connected": self.is_connected,
            "token_count": self.token_count,
        }
