"""Main scanner monitor for token discovery."""
import asyncio
from typing import Optional, List, Callable
from datetime import datetime
from loguru import logger

from api import AxiomAPIClient
from models import TokenModel, FilterConfigModel
from database.repository import TokenRepository, DeveloperRepository, EventRepository, FilterConfigRepository
from filters import FilterEngine
from scanner.stream import WebSocketStream
from scanner.state import ScannerState, ScannerStateManager
from sqlalchemy.orm import Session


class TokenScanner:
    """Main token scanner monitor."""

    def __init__(
        self,
        api_client: AxiomAPIClient,
        db_session: Session,
        on_token_matched: Optional[Callable] = None,
    ):
        """Initialize scanner.

        Args:
            api_client: Axiom API client
            db_session: Database session
            on_token_matched: Callback when token matches filter
        """
        self.api_client = api_client
        self.db_session = db_session
        self.on_token_matched = on_token_matched

        # Initialize repositories
        self.token_repo = TokenRepository(db_session)
        self.dev_repo = DeveloperRepository(db_session)
        self.event_repo = EventRepository(db_session)
        self.filter_repo = FilterConfigRepository(db_session)

        # Initialize filter engine
        self.filter_engine = FilterEngine(db_session)

        # Initialize WebSocket stream
        self.stream = WebSocketStream(self._on_token_received)

        # State management
        self.state_manager = ScannerStateManager()
        self.state_manager.set_stat("start_time", datetime.utcnow().isoformat())

        # Reconnection settings
        self.reconnect_delay = 5
        self.max_reconnects = 10
        self.reconnect_count = 0
        self.is_running = False

    async def start(self) -> None:
        """Start scanning for tokens."""
        logger.info("Starting token scanner")
        self.is_running = True
        self.state_manager.set_state(ScannerState.CONNECTING)

        try:
            # Initialize API client
            await self.api_client.initialize_websocket()
            self.state_manager.set_state(ScannerState.CONNECTED)
            logger.info("Connected to Axiom API")

            # Subscribe to new tokens
            await self.api_client.subscribe_new_tokens(self._handle_token)
            self.state_manager.set_state(ScannerState.SCANNING)
            logger.info("Subscribed to new tokens")

            # Start WebSocket
            await self.api_client.start_websocket()
        except Exception as e:
            logger.error(f"Failed to start scanner: {e}")
            self.state_manager.set_state(ScannerState.ERROR, str(e))
            await self._reconnect()

    async def _handle_token(self, token_data: dict) -> None:
        """Handle new token from API.

        Args:
            token_data: Raw token data from API
        """
        try:
            await self.stream.handle_message(token_data)
        except Exception as e:
            logger.error(f"Error handling token: {e}")

    async def _on_token_received(self, token: TokenModel) -> None:
        """Process received token.

        Args:
            token: Parsed token model
        """
        try:
            self.state_manager.increment_stat("tokens_found")

            # Save to database
            self.token_repo.create_or_update(token)

            # Get enabled filters
            filters = self.filter_repo.get_enabled()
            if not filters:
                logger.debug("No enabled filters")
                return

            # Evaluate against filters
            results = self.filter_engine.evaluate_token(token, filters)
            self.state_manager.increment_stat("filters_applied", len(filters))

            # Check if matched
            if results["matched"]:
                self.state_manager.increment_stat("tokens_matched")
                self.token_repo.update_matched_filters(token.mint_address, results["matched"])

                # Call callback
                if self.on_token_matched:
                    await self.on_token_matched(token, results["matched"])

                logger.info(f"Token {token.symbol} matched filters: {results['matched']}")
        except Exception as e:
            logger.error(f"Error processing token: {e}")

    async def stop(self) -> None:
        """Stop scanning."""
        logger.info("Stopping scanner")
        self.is_running = False
        self.state_manager.set_state(ScannerState.STOPPED)
        await self.api_client.close()
        logger.info("Scanner stopped")

    async def _reconnect(self) -> None:
        """Attempt to reconnect."""
        if not self.is_running:
            return

        if self.reconnect_count >= self.max_reconnects:
            logger.error(f"Max reconnection attempts ({self.max_reconnects}) reached")
            self.state_manager.set_state(ScannerState.ERROR, "Max reconnection attempts reached")
            return

        self.reconnect_count += 1
        self.state_manager.increment_stat("reconnect_count")
        logger.warning(f"Reconnecting... (Attempt {self.reconnect_count}/{self.max_reconnects})")

        await asyncio.sleep(self.reconnect_delay * (2 ** (self.reconnect_count - 1)))
        await self.start()

    def get_status(self) -> dict:
        """Get scanner status.

        Returns:
            Status dictionary
        """
        return self.state_manager.get_status()

    def get_stats(self) -> dict:
        """Get scanner statistics.

        Returns:
            Statistics dictionary
        """
        return self.state_manager.get_stats()
