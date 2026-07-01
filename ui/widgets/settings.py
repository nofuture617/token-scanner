"""Settings widget."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox,
    QSpinBox, QDoubleSpinBox, QPushButton, QGroupBox, QScrollArea
)
from PySide6.QtCore Qt
from loguru import logger


class SettingsWidget(QWidget):
    """Widget for application settings."""

    def __init__(self):
        """Initialize settings widget."""
        super().__init__()
        self.init_ui()

    def init_ui(self) -> None:
        """Initialize UI."""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        # API Settings
        api_group = QGroupBox("🔑 API Settings")
        api_layout = QVBoxLayout()
        
        api_layout.addWidget(QLabel("API Timeout (seconds):"))
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setValue(30)
        api_layout.addWidget(self.timeout_spin)
        
        api_group.setLayout(api_layout)
        main_layout.addWidget(api_group)

        # Browser Settings
        browser_group = QGroupBox("🌐 Browser Settings")
        browser_layout = QVBoxLayout()
        
        self.auto_open_check = QCheckBox("Auto-open matching tokens")
        self.auto_open_check.setChecked(True)
        browser_layout.addWidget(self.auto_open_check)
        
        self.new_tab_check = QCheckBox("Open in new tab")
        self.new_tab_check.setChecked(True)
        browser_layout.addWidget(self.new_tab_check)
        
        browser_group.setLayout(browser_layout)
        main_layout.addWidget(browser_group)

        # Notification Settings
        notif_group = QGroupBox("🔔 Notifications")
        notif_layout = QVBoxLayout()
        
        self.desktop_notif_check = QCheckBox("Desktop notifications")
        self.desktop_notif_check.setChecked(True)
        notif_layout.addWidget(self.desktop_notif_check)
        
        self.sound_notif_check = QCheckBox("Sound notifications")
        self.sound_notif_check.setChecked(True)
        notif_layout.addWidget(self.sound_notif_check)
        
        notif_group.setLayout(notif_layout)
        main_layout.addWidget(notif_group)

        # Database Settings
        db_group = QGroupBox("💾 Database")
        db_layout = QVBoxLayout()
        
        db_layout.addWidget(QLabel("Log retention (days):"))
        self.retention_spin = QSpinBox()
        self.retention_spin.setValue(30)
        db_layout.addWidget(self.retention_spin)
        
        db_group.setLayout(db_layout)
        main_layout.addWidget(db_group)

        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("💾 Save Settings")
        save_btn.clicked.connect(self._on_save_settings)
        btn_layout.addWidget(save_btn)
        
        reset_btn = QPushButton("🔄 Reset to Defaults")
        reset_btn.clicked.connect(self._on_reset_settings)
        btn_layout.addWidget(reset_btn)
        main_layout.addLayout(btn_layout)

        main_layout.addStretch()
        main_widget.setLayout(main_layout)
        scroll_area.setWidget(main_widget)
        
        layout = QVBoxLayout(self)
        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def _on_save_settings(self) -> None:
        """Handle save settings button."""
        logger.info("Settings saved")

    def _on_reset_settings(self) -> None:
        """Handle reset settings button."""
        logger.info("Settings reset to defaults")
