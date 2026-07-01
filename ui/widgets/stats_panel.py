"""Statistics panel widget."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QGroupBox
from PySide6.QtCore Qt, QTimer
from PySide6.QtGui QFont, QColor
from loguru import logger


class StatsPanelWidget(QWidget):
    """Widget for displaying statistics."""

    def __init__(self):
        """Initialize statistics panel."""
        super().__init__()
        self.init_ui()
        self.stats = {}

    def init_ui(self) -> None:
        """Initialize UI."""
        layout = QVBoxLayout()

        # Main statistics
        stats_group = QGroupBox("📊 Scanner Statistics")
        stats_layout = QVBoxLayout()

        # Tokens found
        self.tokens_found_label = self._create_stat_label("Tokens Found", "0")
        stats_layout.addWidget(self.tokens_found_label)

        # Tokens matched
        self.tokens_matched_label = self._create_stat_label("Tokens Matched", "0")
        stats_layout.addWidget(self.tokens_matched_label)

        # Match rate
        self.match_rate_label = self._create_stat_label("Match Rate", "0%")
        stats_layout.addWidget(self.match_rate_label)

        # Notifications sent
        self.notifications_label = self._create_stat_label("Notifications Sent", "0")
        stats_layout.addWidget(self.notifications_label)

        # Uptime
        self.uptime_label = self._create_stat_label("Uptime", "00:00:00")
        stats_layout.addWidget(self.uptime_label)

        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)

        # Developer statistics
        dev_group = QGroupBox("👨‍💻 Top Developers")
        dev_layout = QVBoxLayout()
        self.dev_list = QLabel("Loading...")
        dev_layout.addWidget(self.dev_list)
        dev_group.setLayout(dev_layout)
        layout.addWidget(dev_group)

        layout.addStretch()
        self.setLayout(layout)

    def _create_stat_label(self, title: str, value: str) -> QWidget:
        """Create statistic label.

        Args:
            title: Title
            value: Value

        Returns:
            Widget containing stat
        """
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 10, QFont.Bold))
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 10))
        value_label.setStyleSheet("color: #4CAF50;")
        
        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(value_label)
        
        return widget

    def update_stats(self, stats: dict) -> None:
        """Update statistics.

        Args:
            stats: Statistics dictionary
        """
        self.stats = stats
        # Update labels (implementation would parse stats dict)
        logger.debug("Statistics updated")
