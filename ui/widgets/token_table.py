"""Token table widget."""
from typing import List, Dict, Any
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QHeaderView
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QColor
from loguru import logger


class TokenTableWidget(QWidget):
    """Widget for displaying tokens in table."""

    def __init__(self):
        """Initialize token table widget."""
        super().__init__()
        self.init_ui()
        self.tokens = {}

    def init_ui(self) -> None:
        """Initialize UI."""
        layout = QVBoxLayout()

        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search tokens...")
        self.search_input.textChanged.connect(self._on_search)
        search_layout.addWidget(self.search_input)

        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self._on_clear)
        search_layout.addWidget(clear_btn)
        layout.addLayout(search_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "Symbol", "Name", "Price", "Market Cap", "Liquidity", 
            "Holders", "Dev %", "Age", "Status", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def add_token(self, token_data: Dict[str, Any]) -> None:
        """Add token to table.

        Args:
            token_data: Token data dictionary
        """
        try:
            mint = token_data.get("mint_address", "")
            if mint in self.tokens:
                return  # Already in table

            self.tokens[mint] = token_data
            row = self.table.rowCount()
            self.table.insertRow(row)

            # Add cells
            symbol = token_data.get("symbol", "N/A")
            name = token_data.get("name", "N/A")
            price = f"${token_data.get('price_usd', 0):.8f}"
            market_cap = f"${token_data.get('market_cap_usd', 0):,.0f}"
            liquidity = f"{token_data.get('liquidity_sol', 0):.2f} SOL"
            holders = str(token_data.get('holders_count', 0))
            dev_pct = f"{token_data.get('dev_ownership_percent', 0):.1f}%"
            age = "Just now"
            status = "🟢 New" if token_data.get('is_migrated') else "🟡 Pending"

            items = [symbol, name, price, market_cap, liquidity, holders, dev_pct, age, status, "View"]
            for col, item_text in enumerate(items):
                item = QTableWidgetItem(item_text)
                if col == 0:  # Symbol column - highlight matched tokens
                    if token_data.get('matched_filters'):
                        item.setBackground(QColor(76, 175, 80, 100))  # Green
                        font = QFont()
                        font.setBold(True)
                        item.setFont(font)
                self.table.setItem(row, col, item)

            logger.debug(f"Added token to table: {symbol}")
        except Exception as e:
            logger.error(f"Error adding token to table: {e}")

    def _on_search(self) -> None:
        """Handle search input change."""
        query = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            match = False
            for col in range(self.table.columnCount() - 1):  # Exclude Actions column
                item = self.table.item(row, col)
                if item and query in item.text().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)

    def _on_clear(self) -> None:
        """Clear all tokens."""
        self.table.setRowCount(0)
        self.tokens.clear()
        logger.info("Cleared token table")
