"""Main application window."""
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QStatusBar
from PySide6.QtGui import QIcon, QKeySequence
from PySide6.QtCore import Qt, pyqtSignal, QThread
from loguru import logger
import asyncio

from ui.widgets.token_table import TokenTableWidget
from ui.widgets.filter_panel import FilterPanelWidget
from ui.widgets.event_log import EventLogWidget
from ui.widgets.stats_panel import StatsPanelWidget
from ui.widgets.settings import SettingsWidget
from ui.styles.dark_theme import apply_dark_theme


class MainWindow(QMainWindow):
    """Main application window."""

    token_found = pyqtSignal(dict)  # Emitted when new token found
    scanner_status_changed = pyqtSignal(str)  # Emitted when scanner status changes

    def __init__(self):
        """Initialize main window."""
        super().__init__()
        self.setWindowTitle("🐍 Token Scanner - Axiom Trade")
        self.setWindowIcon(QIcon("assets/icon.png"))
        self.setGeometry(100, 100, 1400, 900)

        # Apply dark theme
        apply_dark_theme(self)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        main_layout = QVBoxLayout(central_widget)

        # Create tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Create tabs
        self.token_table = TokenTableWidget()
        self.filter_panel = FilterPanelWidget()
        self.event_log = EventLogWidget()
        self.stats_panel = StatsPanelWidget()
        self.settings_widget = SettingsWidget()

        # Add tabs
        self.tabs.addTab(self.token_table, "📊 Tokens")
        self.tabs.addTab(self.filter_panel, "🔍 Filters")
        self.tabs.addTab(self.event_log, "📝 Events")
        self.tabs.addTab(self.stats_panel, "📈 Statistics")
        self.tabs.addTab(self.settings_widget, "⚙️ Settings")

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Connect signals
        self.token_found.connect(self._on_token_found)
        self.scanner_status_changed.connect(self._on_scanner_status_changed)

        logger.info("Main window created")

    def _on_token_found(self, token_data: dict) -> None:
        """Handle new token found.

        Args:
            token_data: Token data dictionary
        """
        try:
            self.token_table.add_token(token_data)
            self.event_log.add_event(
                event_type="token_found",
                message=f"New token: {token_data.get('symbol', 'Unknown')}",
            )
        except Exception as e:
            logger.error(f"Error handling token found: {e}")

    def _on_scanner_status_changed(self, status: str) -> None:
        """Handle scanner status change.

        Args:
            status: New status
        """
        self.status_bar.showMessage(f"Scanner: {status}")
        self.event_log.add_event(event_type="status", message=f"Scanner {status}")

    def closeEvent(self, event):
        """Handle window close event.

        Args:
            event: Close event
        """
        logger.info("Closing main window")
        event.accept()
