"""
Modern Application Styles - Cursor/Ant Design Inspired
أنماط حديثة مستوحاة من Cursor و Ant Design
"""

# Modern Light Theme - Clean and Professional
MODERN_LIGHT_THEME = """
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
    font-size: 13px;
}

/* Tab Widget - Modern Design */
QTabWidget::pane {
    border: none;
    background-color: #ffffff;
    border-radius: 0px;
}

QTabBar {
    background-color: #f9fafb;
    border-bottom: 1px solid #e5e7eb;
}

QTabBar::tab {
    background-color: transparent;
    color: #6b7280;
    padding: 12px 20px;
    margin-right: 4px;
    border: none;
    border-bottom: 2px solid transparent;
    font-weight: 500;
    font-size: 13px;
    min-width: 80px;
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

/* Buttons - Modern Gradient Style */
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

/* Input Fields - Modern Design */
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
    outline: none;
}

QLineEdit::placeholder, QTextEdit::placeholder {
    color: #9ca3af;
}

/* Scroll Area - Clean Design */
QScrollArea {
    border: none;
    background-color: #ffffff;
}

QScrollBar:vertical {
    border: none;
    background-color: #f3f4f6;
    width: 10px;
    border-radius: 5px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #d1d5db;
    border-radius: 5px;
    min-height: 30px;
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
    background-color: #f3f4f6;
    height: 10px;
    border-radius: 5px;
    margin: 0px;
}

QScrollBar::handle:horizontal {
    background-color: #d1d5db;
    border-radius: 5px;
    min-width: 30px;
    margin: 2px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #9ca3af;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Tree View - Modern File Browser */
QTreeView {
    border: none;
    background-color: #ffffff;
    selection-background-color: #eff6ff;
    selection-color: #1e40af;
    outline: none;
    font-size: 13px;
}

QTreeView::item {
    padding: 6px;
    border-radius: 4px;
}

QTreeView::item:hover {
    background-color: #f3f4f6;
}

QTreeView::item:selected {
    background-color: #eff6ff;
    color: #1e40af;
}

/* Table Widget - Clean Tables */
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

/* Group Box - Modern Cards */
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

/* Progress Bar - Modern Design */
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

/* ComboBox - Modern Dropdown */
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

QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #6b7280;
    width: 0px;
    height: 0px;
}

QComboBox QAbstractItemView {
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    background-color: #ffffff;
    selection-background-color: #eff6ff;
    selection-color: #1e40af;
    padding: 4px;
}

/* CheckBox - Modern Toggle */
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
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEzLjMzMzMgNEw2IDEyTDIuNjY2NjcgOC42NjY2NyIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
}

/* SpinBox - Modern Number Input */
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

/* Status Bar - Clean Design */
QStatusBar {
    background-color: #f9fafb;
    border-top: 1px solid #e5e7eb;
    color: #6b7280;
    font-size: 12px;
    padding: 4px;
}

/* Menu Bar - Modern Design */
QMenuBar {
    background-color: #ffffff;
    border-bottom: 1px solid #e5e7eb;
    color: #374151;
    padding: 4px;
    font-size: 13px;
}

QMenuBar::item {
    padding: 8px 12px;
    border-radius: 6px;
}

QMenuBar::item:selected {
    background-color: #f3f4f6;
    color: #111827;
}

QMenu {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 4px;
    color: #374151;
}

QMenu::item {
    padding: 8px 24px;
    border-radius: 6px;
}

QMenu::item:selected {
    background-color: #eff6ff;
    color: #1e40af;
}

QMenu::separator {
    height: 1px;
    background-color: #e5e7eb;
    margin: 4px 8px;
}

/* Toolbar - Clean Design */
QToolBar {
    background-color: #ffffff;
    border: none;
    border-bottom: 1px solid #e5e7eb;
    spacing: 4px;
    padding: 8px;
}

QToolBar::separator {
    background-color: #e5e7eb;
    width: 1px;
    margin: 4px 8px;
}

/* Splitter - Modern Handle */
QSplitter::handle {
    background-color: #f3f4f6;
}

QSplitter::handle:horizontal {
    width: 2px;
}

QSplitter::handle:vertical {
    height: 2px;
}

QSplitter::handle:hover {
    background-color: #d1d5db;
}
"""

# Modern Dark Theme - Professional Dark Mode
MODERN_DARK_THEME = """
/* Main Window */
QMainWindow {
    background-color: #0f172a;
    font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Base Widget */
QWidget {
    background-color: #0f172a;
    color: #f1f5f9;
    font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 13px;
}

/* Tab Widget - Dark Design */
QTabWidget::pane {
    border: none;
    background-color: #1e293b;
    border-radius: 0px;
}

QTabBar {
    background-color: #1e293b;
    border-bottom: 1px solid #334155;
}

QTabBar::tab {
    background-color: transparent;
    color: #94a3b8;
    padding: 12px 20px;
    margin-right: 4px;
    border: none;
    border-bottom: 2px solid transparent;
    font-weight: 500;
    font-size: 13px;
    min-width: 80px;
}

QTabBar::tab:selected {
    background-color: #0f172a;
    color: #f1f5f9;
    border-bottom: 2px solid #60a5fa;
    font-weight: 600;
}

QTabBar::tab:hover {
    background-color: #334155;
    color: #cbd5e1;
}

/* Buttons - Dark Theme */
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
    background-color: #334155;
    color: #64748b;
}

/* Input Fields - Dark Design */
QLineEdit, QTextEdit {
    border: 1px solid #475569;
    border-radius: 8px;
    padding: 10px 14px;
    background-color: #1e293b;
    color: #f1f5f9;
    font-size: 14px;
    selection-background-color: #1e40af;
}

QLineEdit:focus, QTextEdit:focus {
    border: 2px solid #60a5fa;
    background-color: #1e293b;
}

QLineEdit::placeholder, QTextEdit::placeholder {
    color: #64748b;
}

/* Scroll Area - Dark Design */
QScrollArea {
    border: none;
    background-color: #0f172a;
}

QScrollBar:vertical {
    border: none;
    background-color: #1e293b;
    width: 10px;
    border-radius: 5px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #475569;
    border-radius: 5px;
    min-height: 30px;
    margin: 2px;
}

QScrollBar::handle:vertical:hover {
    background-color: #64748b;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Tree View - Dark File Browser */
QTreeView {
    border: none;
    background-color: #1e293b;
    selection-background-color: #1e3a8a;
    selection-color: #dbeafe;
    outline: none;
    font-size: 13px;
    color: #f1f5f9;
}

QTreeView::item {
    padding: 6px;
    border-radius: 4px;
}

QTreeView::item:hover {
    background-color: #334155;
}

QTreeView::item:selected {
    background-color: #1e3a8a;
    color: #dbeafe;
}

/* Table Widget - Dark Tables */
QTableWidget {
    border: none;
    background-color: #1e293b;
    gridline-color: #334155;
    font-size: 13px;
    color: #f1f5f9;
}

QTableWidget::item {
    padding: 8px;
    border: none;
}

QTableWidget::item:selected {
    background-color: #1e3a8a;
    color: #dbeafe;
}

QHeaderView::section {
    background-color: #1e293b;
    color: #cbd5e1;
    padding: 10px;
    border: none;
    border-bottom: 2px solid #334155;
    font-weight: 600;
    font-size: 12px;
}

/* Group Box - Dark Cards */
QGroupBox {
    border: 1px solid #334155;
    border-radius: 12px;
    margin-top: 20px;
    padding-top: 20px;
    background-color: #1e293b;
    font-weight: 600;
    font-size: 14px;
    color: #f1f5f9;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 16px;
    padding: 0 8px;
    background-color: #1e293b;
    color: #f1f5f9;
}

/* Progress Bar - Dark Design */
QProgressBar {
    border: none;
    border-radius: 8px;
    text-align: center;
    background-color: #1e293b;
    height: 8px;
    color: #94a3b8;
    font-size: 11px;
    font-weight: 500;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #60a5fa, stop:1 #3b82f6);
    border-radius: 8px;
}

/* ComboBox - Dark Dropdown */
QComboBox {
    border: 1px solid #475569;
    border-radius: 8px;
    padding: 8px 12px;
    background-color: #1e293b;
    color: #f1f5f9;
    font-size: 13px;
    min-height: 36px;
}

QComboBox:hover {
    border: 1px solid #64748b;
}

QComboBox:focus {
    border: 2px solid #60a5fa;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #94a3b8;
    width: 0px;
    height: 0px;
}

QComboBox QAbstractItemView {
    border: 1px solid #334155;
    border-radius: 8px;
    background-color: #1e293b;
    selection-background-color: #1e3a8a;
    selection-color: #dbeafe;
    padding: 4px;
}

/* CheckBox - Dark Toggle */
QCheckBox {
    spacing: 10px;
    color: #cbd5e1;
    font-size: 13px;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border: 2px solid #475569;
    border-radius: 6px;
    background-color: #1e293b;
}

QCheckBox::indicator:hover {
    border: 2px solid #64748b;
}

QCheckBox::indicator:checked {
    background-color: #3b82f6;
    border: 2px solid #3b82f6;
}

/* SpinBox - Dark Number Input */
QSpinBox {
    border: 1px solid #475569;
    border-radius: 8px;
    padding: 8px 12px;
    background-color: #1e293b;
    color: #f1f5f9;
    font-size: 13px;
    min-height: 36px;
}

QSpinBox:focus {
    border: 2px solid #60a5fa;
}

QSpinBox::up-button, QSpinBox::down-button {
    border: none;
    background-color: #334155;
    border-radius: 4px;
    width: 20px;
}

QSpinBox::up-button:hover, QSpinBox::down-button:hover {
    background-color: #475569;
}

/* Status Bar - Dark Design */
QStatusBar {
    background-color: #1e293b;
    border-top: 1px solid #334155;
    color: #94a3b8;
    font-size: 12px;
    padding: 4px;
}

/* Menu Bar - Dark Design */
QMenuBar {
    background-color: #1e293b;
    border-bottom: 1px solid #334155;
    color: #cbd5e1;
    padding: 4px;
    font-size: 13px;
}

QMenuBar::item {
    padding: 8px 12px;
    border-radius: 6px;
}

QMenuBar::item:selected {
    background-color: #334155;
    color: #f1f5f9;
}

QMenu {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 4px;
    color: #cbd5e1;
}

QMenu::item {
    padding: 8px 24px;
    border-radius: 6px;
}

QMenu::item:selected {
    background-color: #1e3a8a;
    color: #dbeafe;
}

QMenu::separator {
    height: 1px;
    background-color: #334155;
    margin: 4px 8px;
}

/* Toolbar - Dark Design */
QToolBar {
    background-color: #1e293b;
    border: none;
    border-bottom: 1px solid #334155;
    spacing: 4px;
    padding: 8px;
}

QToolBar::separator {
    background-color: #334155;
    width: 1px;
    margin: 4px 8px;
}

/* Splitter - Dark Handle */
QSplitter::handle {
    background-color: #334155;
}

QSplitter::handle:horizontal {
    width: 2px;
}

QSplitter::handle:vertical {
    height: 2px;
}

QSplitter::handle:hover {
    background-color: #475569;
}
"""

