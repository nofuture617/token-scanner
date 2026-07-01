"""API client wrapper for Axiom Trade."""
import asyncio
from typing import Optional, Dict, Any, Callable
from loguru import logger
from axiomtradeapi import AxiomTradeClient, AxiomTradeWebSocketClient
from axiomtradeapi.auth.login import AxiomAuth


class AxiomAPIClient:
    """Wrapper for Axiom Trade API client."""

    def __init__(self, access_token: str, refresh_token: str):
        """Initialize Axiom API client.

        Args:
            access_token: API access token
            refresh_token: API refresh token
        """
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.client = None
        self.ws_client = None

    def initialize(self) -> None:
        """Initialize API clients."""
        try:
            self.client = AxiomTradeClient(
                auth_token=self.access_token,
                refresh_token=self.refresh_token,
            )
            logger.info("Axiom API client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Axiom API client: {e}")
            raise

    async def initialize_websocket(self) -> None:
        """Initialize WebSocket client."""
        try:
            auth_manager = AxiomAuth(
                auth_token=self.access_token,
                refresh_token=self.refresh_token,
            )
            self.ws_client = AxiomTradeWebSocketClient(auth_manager)
            logger.info("Axiom WebSocket client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize WebSocket client: {e}")
            raise

    async def subscribe_new_tokens(self, callback: Callable) -> bool:
        """Subscribe to new token updates.

        Args:
            callback: Callback function for new tokens

        Returns:
            True if subscription successful
        """
        if not self.ws_client:
            await self.initialize_websocket()
        
        try:
            result = await self.ws_client.subscribe_new_tokens(callback)
            if result:
                logger.info("Subscribed to new tokens")
            return result
        except Exception as e:
            logger.error(f"Failed to subscribe to new tokens: {e}")
            return False

    async def start_websocket(self) -> None:
        """Start WebSocket connection."""
        if not self.ws_client:
            await self.initialize_websocket()
        
        try:
            await self.ws_client.start()
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            raise

    def get_client(self) -> Optional[AxiomTradeClient]:
        """Get REST API client.

        Returns:
            Axiom API client or None
        """
        if not self.client:
            self.initialize()
        return self.client

    async def close(self) -> None:
        """Close all connections."""
        if self.ws_client:
            try:
                await self.ws_client.close()
            except Exception as e:
                logger.error(f"Error closing WebSocket: {e}")
        logger.info("API connections closed")
