"""
Cursor-Inspired Modern Styles
أنماط حديثة مستوحاة من Cursor
"""

# Cursor-like Light Theme - Clean, Professional, Light Colors
CURSOR_LIGHT_THEME = """
/* Main Window */
QMainWindow {
    background-color: #ffffff;
    font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Base Widget */
QWidget {
    background-color: #ffffff;
    color: #1f2937;
    font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Menu Bar - Top Menu */
QMenuBar {
    background-color: #ffffff;
    border-bottom: 1px solid #e5e7eb;
    color: #374151;
    padding: 4px 8px;
    font-size: 13px;
    font-weight: 500;
}

QMenuBar::item {
    padding: 8px 12px;
    border-radius: 6px;
    spacing: 4px;
}

QMenuBar::item:selected {
    background-color: #f3f4f6;
    color: #111827;
}

QMenu {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 6px;
    color: #374151;
    font-size: 13px;
}

QMenu::item {
    padding: 8px 24px 8px 32px;
    border-radius: 6px;
    min-width: 150px;
}

QMenu::item:selected {
    background-color: #eff6ff;
    color: #1e40af;
}

QMenu::separator {
    height: 1px;
    background-color: #e5e7eb;
    margin: 6px 8px;
}

/* Toolbar */
QToolBar {
    background-color: #ffffff;
    border: none;
    border-bottom: 1px solid #e5e7eb;
    spacing: 8px;
    padding: 8px 12px;
}

QToolBar::separator {
    background-color: #e5e7eb;
    width: 1px;
    margin: 4px 8px;
}

/* Tab Widget - Modern Tabs */
QTabWidget::pane {
    border: none;
    background-color: #ffffff;
    top: -1px;
}

QTabBar {
    background-color: #f9fafb;
    border-bottom: 1px solid #e5e7eb;
}

QTabBar::tab {
    background-color: transparent;
    color: #6b7280;
    padding: 10px 20px;
    margin-right: 2px;
    border: none;
    border-bottom: 2px solid transparent;
    font-weight: 500;
    font-size: 13px;
    min-width: 70px;
}

QTabBar::tab:selected {
    background-color: #ffffff;
    color: #111827;
    border-bottom: 2px solid #3b82f6;
    font-weight: 600;
}

QTabBar::tab:hover {
    background-color: #f3f4f6;
    color: #374151;
}

/* Buttons - Modern Gradient */
QPushButton {
    background-color: #3b82f6;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    font-weight: 500;
    font-size: 13px;
    min-height: 36px;
}

QPushButton:hover {
    background-color: #2563eb;
}

QPushButton:pressed {
    background-color: #1d4ed8;
}

QPushButton:disabled {
    background-color: #e5e7eb;
    color: #9ca3af;
}

/* Input Fields */
QLineEdit, QTextEdit {
    border: 1px solid #d1d5db;
    border-radius: 8px;
    padding: 10px 14px;
    background-color: #ffffff;
    color: #111827;
    font-size: 14px;
    selection-background-color: #dbeafe;
}

QLineEdit:focus, QTextEdit:focus {
    border: 2px solid #3b82f6;
    background-color: #ffffff;
}

QLineEdit::placeholder, QTextEdit::placeholder {
    color: #9ca3af;
}

/* Scroll Bars - Thin and Modern */
QScrollBar:vertical {
    border: none;
    background-color: #f9fafb;
    width: 8px;
    border-radius: 4px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #d1d5db;
    border-radius: 4px;
    min-height: 20px;
    margin: 2px;
}

QScrollBar::handle:vertical:hover {
    background-color: #9ca3af;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background-color: #f9fafb;
    height: 8px;
    border-radius: 4px;
    margin: 0px;
}

QScrollBar::handle:horizontal {
    background-color: #d1d5db;
    border-radius: 4px;
    min-width: 20px;
    margin: 2px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #9ca3af;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Tree View - File Browser */
QTreeView {
    border: none;
    background-color: #f9fafb;
    selection-background-color: #eff6ff;
    selection-color: #1e40af;
    outline: none;
    font-size: 13px;
    alternate-background-color: #ffffff;
}

QTreeView::item {
    padding: 4px;
    border-radius: 4px;
}

QTreeView::item:hover {
    background-color: #f3f4f6;
}

QTreeView::item:selected {
    background-color: #eff6ff;
    color: #1e40af;
}

/* Table Widget */
QTableWidget {
    border: none;
    background-color: #ffffff;
    gridline-color: #f3f4f6;
    font-size: 13px;
}

QTableWidget::item {
    padding: 8px;
    border: none;
}

QTableWidget::item:selected {
    background-color: #eff6ff;
    color: #1e40af;
}

QHeaderView::section {
    background-color: #f9fafb;
    color: #374151;
    padding: 10px;
    border: none;
    border-bottom: 2px solid #e5e7eb;
    font-weight: 600;
    font-size: 12px;
}

/* Group Box */
QGroupBox {
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    margin-top: 20px;
    padding-top: 20px;
    background-color: #ffffff;
    font-weight: 600;
    font-size: 14px;
    color: #111827;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 16px;
    padding: 0 8px;
    background-color: #ffffff;
    color: #111827;
}

/* Progress Bar */
QProgressBar {
    border: none;
    border-radius: 8px;
    text-align: center;
    background-color: #f3f4f6;
    height: 8px;
    color: #6b7280;
    font-size: 11px;
    font-weight: 500;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #3b82f6, stop:1 #60a5fa);
    border-radius: 8px;
}

/* ComboBox */
QComboBox {
    border: 1px solid #d1d5db;
    border-radius: 8px;
    padding: 8px 12px;
    background-color: #ffffff;
    color: #111827;
    font-size: 13px;
    min-height: 36px;
}

QComboBox:hover {
    border: 1px solid #9ca3af;
}

QComboBox:focus {
    border: 2px solid #3b82f6;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox QAbstractItemView {
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    background-color: #ffffff;
    selection-background-color: #eff6ff;
    selection-color: #1e40af;
    padding: 4px;
}

/* CheckBox */
QCheckBox {
    spacing: 10px;
    color: #374151;
    font-size: 13px;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border: 2px solid #d1d5db;
    border-radius: 6px;
    background-color: #ffffff;
}

QCheckBox::indicator:hover {
    border: 2px solid #9ca3af;
}

QCheckBox::indicator:checked {
    background-color: #3b82f6;
    border: 2px solid #3b82f6;
}

/* SpinBox */
QSpinBox {
    border: 1px solid #d1d5db;
    border-radius: 8px;
    padding: 8px 12px;
    background-color: #ffffff;
    color: #111827;
    font-size: 13px;
    min-height: 36px;
}

QSpinBox:focus {
    border: 2px solid #3b82f6;
}

QSpinBox::up-button, QSpinBox::down-button {
    border: none;
    background-color: #f3f4f6;
    border-radius: 4px;
    width: 20px;
}

QSpinBox::up-button:hover, QSpinBox::down-button:hover {
    background-color: #e5e7eb;
}

/* Status Bar */
QStatusBar {
    background-color: #f9fafb;
    border-top: 1px solid #e5e7eb;
    color: #6b7280;
    font-size: 12px;
    padding: 4px 8px;
}

/* Splitter */
QSplitter::handle {
    background-color: #e5e7eb;
}

QSplitter::handle:horizontal {
    width: 1px;
}

QSplitter::handle:vertical {
    height: 1px;
}

QSplitter::handle:hover {
    background-color: #d1d5db;
}
"""

