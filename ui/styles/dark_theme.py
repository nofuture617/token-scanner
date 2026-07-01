"""Dark theme stylesheet."""

DARK_THEME_QSS = """
    QMainWindow {
        background-color: #1e1e1e;
        color: #e0e0e0;
    }
    
    QWidget {
        background-color: #1e1e1e;
        color: #e0e0e0;
    }
    
    QTabWidget::pane {
        border: 1px solid #404040;
    }
    
    QTabBar::tab {
        background-color: #2d2d2d;
        color: #e0e0e0;
        padding: 8px 20px;
        border: 1px solid #404040;
    }
    
    QTabBar::tab:selected {
        background-color: #4CAF50;
        color: #ffffff;
        border-bottom: 2px solid #4CAF50;
    }
    
    QTableWidget {
        background-color: #1e1e1e;
        alternate-background-color: #2d2d2d;
        gridline-color: #404040;
    }
    
    QTableWidget::item {
        padding: 5px;
        color: #e0e0e0;
    }
    
    QTableWidget::item:selected {
        background-color: #4CAF50;
        color: #ffffff;
    }
    
    QHeaderView::section {
        background-color: #2d2d2d;
        color: #e0e0e0;
        padding: 5px;
        border: 1px solid #404040;
    }
    
    QLineEdit, QTextEdit {
        background-color: #2d2d2d;
        color: #e0e0e0;
        border: 1px solid #404040;
        border-radius: 4px;
        padding: 5px;
    }
    
    QLineEdit:focus, QTextEdit:focus {
        border: 1px solid #4CAF50;
        background-color: #2d2d2d;
    }
    
    QPushButton {
        background-color: #4CAF50;
        color: #ffffff;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: bold;
    }
    
    QPushButton:hover {
        background-color: #45a049;
    }
    
    QPushButton:pressed {
        background-color: #3d8b40;
    }
    
    QCheckBox {
        color: #e0e0e0;
        spacing: 5px;
    }
    
    QCheckBox::indicator {
        width: 16px;
        height: 16px;
    }
    
    QCheckBox::indicator:unchecked {
        background-color: #2d2d2d;
        border: 1px solid #404040;
        border-radius: 3px;
    }
    
    QCheckBox::indicator:checked {
        background-color: #4CAF50;
        border: 1px solid #4CAF50;
        border-radius: 3px;
    }
    
    QGroupBox {
        color: #e0e0e0;
        border: 1px solid #404040;
        border-radius: 4px;
        margin-top: 10px;
        padding-top: 10px;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 3px 0 3px;
    }
    
    QComboBox {
        background-color: #2d2d2d;
        color: #e0e0e0;
        border: 1px solid #404040;
        border-radius: 4px;
        padding: 5px;
    }
    
    QComboBox::drop-down {
        border: none;
    }
    
    QComboBox QAbstractItemView {
        background-color: #2d2d2d;
        color: #e0e0e0;
        selection-background-color: #4CAF50;
    }
    
    QSpinBox, QDoubleSpinBox {
        background-color: #2d2d2d;
        color: #e0e0e0;
        border: 1px solid #404040;
        border-radius: 4px;
        padding: 5px;
    }
    
    QStatusBar {
        background-color: #2d2d2d;
        color: #e0e0e0;
        border-top: 1px solid #404040;
    }
    
    QLabel {
        color: #e0e0e0;
    }
    
    QScrollBar:vertical {
        border: none;
        background-color: #2d2d2d;
        width: 12px;
        margin: 0px 0px 0px 0px;
    }
    
    QScrollBar::handle:vertical {
        background-color: #404040;
        border-radius: 6px;
        min-height: 20px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #505050;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: none;
        background: none;
    }
"""


def apply_dark_theme(app):
    """Apply dark theme to application.

    Args:
        app: QApplication instance
    """
    app.setStyleSheet(DARK_THEME_QSS)
