"""Filter panel widget."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox,
    QCheckBox, QPushButton, QGroupBox, QScrollArea, QListWidget, QListWidgetItem
)
from PySide6.QtCore Qt
from loguru import logger


class FilterPanelWidget(QWidget):
    """Widget for filter management."""

    def __init__(self):
        """Initialize filter panel."""
        super().__init__()
        self.init_ui()

    def init_ui(self) -> None:
        """Initialize UI."""
        main_layout = QVBoxLayout()

        # Active filters list
        list_label = QLabel("📋 Active Filters")
        self.filters_list = QListWidget()
        main_layout.addWidget(list_label)
        main_layout.addWidget(self.filters_list)

        # Filter controls
        controls_group = QGroupBox("Create New Filter")
        controls_layout = QVBoxLayout()

        # Min liquidity
        liq_layout = QHBoxLayout()
        liq_layout.addWidget(QLabel("Min Liquidity (SOL):"))
        self.min_liq_spin = QDoubleSpinBox()
        self.min_liq_spin.setValue(2.0)
        self.min_liq_spin.setMaximum(1000.0)
        liq_layout.addWidget(self.min_liq_spin)
        controls_layout.addLayout(liq_layout)

        # Min market cap
        mcap_layout = QHBoxLayout()
        mcap_layout.addWidget(QLabel("Min Market Cap (USD):"))
        self.min_mcap_spin = QDoubleSpinBox()
        self.min_mcap_spin.setMaximum(10000000.0)
        mcap_layout.addWidget(self.min_mcap_spin)
        controls_layout.addLayout(mcap_layout)

        # Dev ownership
        dev_layout = QHBoxLayout()
        dev_layout.addWidget(QLabel("Max Dev Ownership (%):"))
        self.max_dev_spin = QDoubleSpinBox()
        self.max_dev_spin.setValue(50.0)
        self.max_dev_spin.setMaximum(100.0)
        dev_layout.addWidget(self.max_dev_spin)
        controls_layout.addLayout(dev_layout)

        # Checkboxes
        self.migrated_only = QCheckBox("Only Migrated Tokens")
        controls_layout.addWidget(self.migrated_only)

        self.no_mint_auth = QCheckBox("No Mint Authority")
        controls_layout.addWidget(self.no_mint_auth)

        self.no_freeze_auth = QCheckBox("No Freeze Authority")
        controls_layout.addWidget(self.no_freeze_auth)

        # Buttons
        btn_layout = QHBoxLayout()
        create_btn = QPushButton("✅ Create Filter")
        create_btn.clicked.connect(self._on_create_filter)
        btn_layout.addWidget(create_btn)

        delete_btn = QPushButton("❌ Delete Filter")
        delete_btn.clicked.connect(self._on_delete_filter)
        btn_layout.addWidget(delete_btn)
        controls_layout.addLayout(btn_layout)

        controls_group.setLayout(controls_layout)
        main_layout.addWidget(controls_group)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def _on_create_filter(self) -> None:
        """Handle create filter button."""
        logger.info("Create filter clicked")
        # Implementation would connect to FilterService

    def _on_delete_filter(self) -> None:
        """Handle delete filter button."""
        logger.info("Delete filter clicked")
