"""Main application entry point."""
import asyncio
import sys
from pathlib import Path
from loguru import logger

from config import get_settings
from utils import setup_logger
from database import DatabaseConnection
from api import AxiomAPIClient
from scanner import TokenScanner
from browser import BrowserManager
from services import (
    TokenService,
    FilterService,
    NotificationService,
    AnalyticsService,
)


class Application:
    """Main application class."""

    def __init__(self):
        """Initialize application."""
        self.settings = get_settings()
        self.db_connection = None
        self.api_client = None
        self.scanner = None
        self.browser_manager = None
        self.notification_service = None

    def setup(self) -> None:
        """Setup application."""
        # Setup logging
        setup_logger(debug=self.settings.app_debug, log_level=self.settings.app_log_level)
        logger.info(f"Initializing {self.settings.app_name} v{self.settings.app_version}")

        # Create directories
        self.settings.ensure_directories()

        # Initialize database
        self.db_connection = DatabaseConnection(self.settings.database_path)
        self.db_connection.initialize()
        self.db_connection.create_tables()
        logger.info("Database initialized")

        # Initialize API client
        self.api_client = AxiomAPIClient(
            access_token=self.settings.axiom_access_token,
            refresh_token=self.settings.axiom_refresh_token,
        )
        self.api_client.initialize()
        logger.info("API client initialized")

        # Initialize browser manager
        self.browser_manager = BrowserManager(
            headless=self.settings.browser_headless,
            auto_open=self.settings.browser_auto_open,
            new_tab=self.settings.browser_new_tab,
        )
        logger.info("Browser manager initialized")

        # Initialize notification service
        self.notification_service = NotificationService(
            desktop_notifications=self.settings.notify_desktop,
            sound_notifications=self.settings.notify_sound,
            sound_path=self.settings.notify_sound_path,
        )
        logger.info("Notification service initialized")

        # Initialize scanner
        self.scanner = TokenScanner(
            api_client=self.api_client,
            db_session=self.db_connection.get_session(),
            on_token_matched=self._on_token_matched,
        )
        logger.info("Scanner initialized")

    async def run(self) -> None:
        """Run application."""
        try:
            logger.info("Starting application")
            await self.scanner.start()
            
            # Keep running
            while self.scanner.is_running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
        except Exception as e:
            logger.error(f"Application error: {e}")
        finally:
            await self.cleanup()

    async def _on_token_matched(self, token, matched_filters: list) -> None:
        """Handle matched token.

        Args:
            token: Token model
            matched_filters: List of matched filter names
        """
        try:
            # Send notification
            await self.notification_service.notify_token_match(
                token_name=token.name,
                token_symbol=token.symbol,
                filters=matched_filters,
            )

            # Open browser if enabled
            if self.settings.browser_auto_open:
                try:
                    await self.browser_manager.initialize()
                    await self.browser_manager.open_token_page(
                        token_mint=token.mint_address,
                        token_name=token.symbol,
                    )
                except Exception as e:
                    logger.error(f"Failed to open browser: {e}")

            logger.info(f"Token matched and processed: {token.symbol}")
        except Exception as e:
            logger.error(f"Error in token match handler: {e}")

    async def cleanup(self) -> None:
        """Cleanup resources."""
        logger.info("Cleaning up resources")
        
        if self.scanner:
            await self.scanner.stop()
        
        if self.browser_manager:
            await self.browser_manager.close()
        
        if self.db_connection:
            self.db_connection.close()
        
        logger.info("Application stopped")


async def main():
    """Main entry point."""
    app = Application()
    app.setup()
    await app.run()


if __name__ == "__main__":
    # Handle CLI arguments
    if "--debug" in sys.argv:
        asyncio.run(main())
    else:
        asyncio.run(main())
