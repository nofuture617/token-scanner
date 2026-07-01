"""Event log widget."""
from typing import Optional
from datetime import datetime
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QComboBox
from PySide6.QtCore Qt
from loguru import logger


class EventLogWidget(QWidget):
    """Widget for event logging."""

    def __init__(self):
        """Initialize event log widget."""
        super().__init__()
        self.init_ui()

    def init_ui(self) -> None:
        """Initialize UI."""
        layout = QVBoxLayout()

        # Controls
        controls_layout = QHBoxLayout()
        
        controls_layout.addWidget(QLabel("Filter:"))
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "Token Found", "Match", "Error", "Status"])
        controls_layout.addWidget(self.filter_combo)
        
        clear_btn = QPushButton("Clear Log")
        clear_btn.clicked.connect(self._on_clear_log)
        controls_layout.addWidget(clear_btn)
        
        layout.addLayout(controls_layout)

        # Log display
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Courier", 9))
        layout.addWidget(self.log_text)

        self.setLayout(layout)

    def add_event(self, event_type: str, message: str) -> None:
        """Add event to log.

        Args:
            event_type: Event type
            message: Event message
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {event_type.upper()}: {message}\n"
        self.log_text.append(log_entry)

    def _on_clear_log(self) -> None:
        """Clear log."""
        self.log_text.clear()
        logger.info("Event log cleared")
