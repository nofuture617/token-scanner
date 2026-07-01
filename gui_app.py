"""Enhanced GUI app with error handling for frozen executable."""
import sys
import asyncio
import traceback
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QThread, pyqtSignal
from loguru import logger

try:
    from config import get_settings
    from utils import setup_logger
    from database import DatabaseConnection
    from api import AxiomAPIClient
    from scanner import TokenScanner
    from ui import MainWindow
except ImportError as e:
    print(f"Import Error: {e}")
    print("Make sure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)


class ScannerThread(QThread):
    """Thread for running scanner."""

    token_found = pyqtSignal(dict)
    status_changed = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, scanner: TokenScanner):
        """Initialize scanner thread.

        Args:
            scanner: Token scanner instance
        """
        super().__init__()
        self.scanner = scanner
        self.running = True

    def run(self) -> None:
        """Run scanner in thread."""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.scanner.start())
        except Exception as e:
            logger.error(f"Scanner thread error: {e}")
            logger.error(traceback.format_exc())
            self.error_occurred.emit(str(e))

    def stop(self) -> None:
        """Stop scanner."""
        self.running = False
        self.wait()


class Application:
    """Main application."""

    def __init__(self):
        """Initialize application."""
        try:
            self.settings = get_settings()
        except Exception as e:
            print(f"Config Error: {e}")
            print("Check .env file exists and contains valid tokens")
            sys.exit(1)
        
        self.qt_app = None
        self.main_window = None
        self.scanner_thread = None
        self.scanner = None
        self.db_connection = None
        self.api_client = None

    def setup(self) -> bool:
        """Setup application.
        
        Returns:
            True if setup successful
        """
        try:
            # Setup logging
            setup_logger(debug=self.settings.app_debug, log_level=self.settings.app_log_level)
            logger.info(f"Initializing {self.settings.app_name} v{self.settings.app_version}")

            # Create directories
            self.settings.ensure_directories()
            logger.info("Directories created")

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

            # Initialize scanner
            self.scanner = TokenScanner(
                api_client=self.api_client,
                db_session=self.db_connection.get_session(),
                on_token_matched=self._on_token_matched,
            )
            logger.info("Scanner initialized")

            # Setup Qt application
            self.qt_app = QApplication(sys.argv)
            self.qt_app.setApplicationName(self.settings.app_name)
            self.qt_app.setApplicationVersion(self.settings.app_version)

            # Create main window
            self.main_window = MainWindow()
            logger.info("Main window created")

            # Create scanner thread
            self.scanner_thread = ScannerThread(self.scanner)
            self.scanner_thread.token_found.connect(self.main_window.token_found.emit)
            self.scanner_thread.status_changed.connect(self.main_window.scanner_status_changed.emit)
            self.scanner_thread.error_occurred.connect(self._on_scanner_error)

            logger.info("Application setup complete")
            return True
        except Exception as e:
            logger.error(f"Setup error: {e}")
            logger.error(traceback.format_exc())
            return False

    async def _on_token_matched(self, token, matched_filters: list) -> None:
        """Handle matched token.

        Args:
            token: Token model
            matched_filters: List of matched filter names
        """
        try:
            token_data = token.dict()
            token_data["matched_filters"] = matched_filters
            self.main_window.token_found.emit(token_data)
        except Exception as e:
            logger.error(f"Error handling token match: {e}")

    def _on_scanner_error(self, error_msg: str) -> None:
        """Handle scanner error.

        Args:
            error_msg: Error message
        """
        logger.error(f"Scanner error: {error_msg}")
        if self.main_window:
            self.main_window.statusBar().showMessage(f"Error: {error_msg}")

    def run(self) -> int:
        """Run application.

        Returns:
            Exit code
        """
        try:
            # Show main window
            self.main_window.show()
            logger.info("Application window shown")

            # Start scanner thread
            self.scanner_thread.start()
            logger.info("Scanner thread started")

            # Run Qt event loop
            return self.qt_app.exec()
        except Exception as e:
            logger.error(f"Application error: {e}")
            logger.error(traceback.format_exc())
            if self.main_window:
                QMessageBox.critical(self.main_window, "Error", f"Application error: {e}")
            return 1
        finally:
            self.cleanup()

    def cleanup(self) -> None:
        """Cleanup resources."""
        logger.info("Cleaning up resources")
        
        if self.scanner_thread:
            self.scanner_thread.stop()
        
        if self.scanner:
            try:
                asyncio.run(self.scanner.stop())
            except:
                pass
        
        if self.db_connection:
            self.db_connection.close()
        
        logger.info("Application stopped")


def main() -> int:
    """Main entry point.

    Returns:
        Exit code
    """
    try:
        app = Application()
        if not app.setup():
            return 1
        return app.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        print(traceback.format_exc())
        return 1


if __name__ == "__main__":
    sys.exit(main())
