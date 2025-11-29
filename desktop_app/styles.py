"""
Application Styles
أنماط التطبيق
"""

# Light theme styles
LIGHT_THEME = """
QMainWindow {
    background-color: #f5f5f5;
    font-family: 'Segoe UI', Arial, sans-serif;
}

QWidget {
    background-color: #f5f5f5;
    color: #212121;
    font-family: 'Segoe UI', Arial, sans-serif;
}

QTabWidget::pane {
    border: 1px solid #ddd;
    background-color: #ffffff;
}

QTabBar::tab {
    background-color: #f0f0f0;
    color: #000000;
    padding: 8px 16px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background-color: #ffffff;
    border-bottom: 2px solid #0078d4;
}

QTabBar::tab:hover {
    background-color: #e0e0e0;
}

QPushButton {
    background-color: #0078d4;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #106ebe;
}

QPushButton:pressed {
    background-color: #005a9e;
}

QPushButton:disabled {
    background-color: #cccccc;
    color: #666666;
}

QLineEdit, QTextEdit {
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 6px;
    background-color: #ffffff;
}

QLineEdit:focus, QTextEdit:focus {
    border: 2px solid #0078d4;
}

QScrollArea {
    border: none;
    background-color: #ffffff;
}

QTreeView {
    border: 1px solid #ddd;
    background-color: #ffffff;
    selection-background-color: #e3f2fd;
}

QTableWidget {
    border: 1px solid #ddd;
    background-color: #ffffff;
    gridline-color: #e0e0e0;
}

QTableWidget::item:selected {
    background-color: #e3f2fd;
    color: #000000;
}

QGroupBox {
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-top: 10px;
    font-weight: bold;
    padding-top: 10px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}

QProgressBar {
    border: 1px solid #ddd;
    border-radius: 4px;
    text-align: center;
    background-color: #f0f0f0;
}

QProgressBar::chunk {
    background-color: #0078d4;
    border-radius: 3px;
}

QComboBox {
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 4px;
    background-color: #ffffff;
}

QComboBox:hover {
    border: 1px solid #0078d4;
}

QCheckBox {
    spacing: 5px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 1px solid #ddd;
    border-radius: 3px;
    background-color: #ffffff;
}

QCheckBox::indicator:checked {
    background-color: #0078d4;
    border: 1px solid #0078d4;
}

QSpinBox {
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 4px;
    background-color: #ffffff;
}

QStatusBar {
    background-color: #f0f0f0;
    border-top: 1px solid #ddd;
}
"""

# Dark theme styles
DARK_THEME = """
QMainWindow {
    background-color: #1e1e1e;
}

QWidget {
    background-color: #1e1e1e;
    color: #ffffff;
}

QTabWidget::pane {
    border: 1px solid #3e3e3e;
    background-color: #1e1e1e;
}

QTabBar::tab {
    background-color: #2d2d2d;
    color: #ffffff;
    padding: 8px 16px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background-color: #1e1e1e;
    border-bottom: 2px solid #0078d4;
}

QTabBar::tab:hover {
    background-color: #3d3d3d;
}

QPushButton {
    background-color: #0078d4;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #106ebe;
}

QPushButton:pressed {
    background-color: #005a9e;
}

QPushButton:disabled {
    background-color: #3d3d3d;
    color: #666666;
}

QLineEdit, QTextEdit {
    border: 1px solid #3e3e3e;
    border-radius: 4px;
    padding: 6px;
    background-color: #2d2d2d;
    color: #ffffff;
}

QLineEdit:focus, QTextEdit:focus {
    border: 2px solid #0078d4;
}

QScrollArea {
    border: none;
    background-color: #1e1e1e;
}

QTreeView {
    border: 1px solid #3e3e3e;
    background-color: #1e1e1e;
    selection-background-color: #264f78;
    color: #ffffff;
}

QTableWidget {
    border: 1px solid #3e3e3e;
    background-color: #1e1e1e;
    gridline-color: #3e3e3e;
    color: #ffffff;
}

QTableWidget::item:selected {
    background-color: #264f78;
    color: #ffffff;
}

QGroupBox {
    border: 1px solid #3e3e3e;
    border-radius: 4px;
    margin-top: 10px;
    font-weight: bold;
    padding-top: 10px;
    color: #ffffff;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}

QProgressBar {
    border: 1px solid #3e3e3e;
    border-radius: 4px;
    text-align: center;
    background-color: #2d2d2d;
    color: #ffffff;
}

QProgressBar::chunk {
    background-color: #0078d4;
    border-radius: 3px;
}

QComboBox {
    border: 1px solid #3e3e3e;
    border-radius: 4px;
    padding: 4px;
    background-color: #2d2d2d;
    color: #ffffff;
}

QComboBox:hover {
    border: 1px solid #0078d4;
}

QCheckBox {
    spacing: 5px;
    color: #ffffff;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 1px solid #3e3e3e;
    border-radius: 3px;
    background-color: #2d2d2d;
}

QCheckBox::indicator:checked {
    background-color: #0078d4;
    border: 1px solid #0078d4;
}

QSpinBox {
    border: 1px solid #3e3e3e;
    border-radius: 4px;
    padding: 4px;
    background-color: #2d2d2d;
    color: #ffffff;
}

QStatusBar {
    background-color: #2d2d2d;
    border-top: 1px solid #3e3e3e;
    color: #ffffff;
}
"""

