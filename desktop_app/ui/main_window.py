"""
Main Window for Desktop Application
النافذة الرئيسية لتطبيق سطح المكتب
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QMenuBar, QStatusBar, QToolBar, QMessageBox, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QSize
from PyQt6.QtGui import QAction, QIcon, QKeySequence
import sys
from pathlib import Path

from desktop_app.ui.project_sidebar import ProjectSidebar


class MainWindow(QMainWindow):
    """Main application window"""
    
    # Signals
    agent_mode_changed = pyqtSignal(str)  # 'simple' or 'expert'
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Local AI Agent - Desktop Application")
        self.setGeometry(100, 100, 1600, 1000)
        # Modern window styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
        """)
        
        # Initialize UI components
        self._init_ui()
        self._create_menu_bar()
        self._create_toolbar()
        self._create_status_bar()
        
        # Store references to widgets
        self.chat_widget = None
        self.file_manager = None
        self.code_editor = None
        self.dashboard = None
        self.settings = None
        
    def _init_ui(self):
        """Initialize the main UI - Cursor-like layout"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main horizontal layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left Sidebar - Project Files
        self.project_sidebar = ProjectSidebar()
        self.project_sidebar.setMinimumWidth(280)
        self.project_sidebar.setMaximumWidth(350)
        self.project_sidebar.setStyleSheet("""
            QWidget {
                background-color: #f9fafb;
                border-right: 1px solid #e5e7eb;
            }
            QTreeView {
                background-color: #f9fafb;
                border: none;
                selection-background-color: #eff6ff;
                selection-color: #1e40af;
                font-size: 13px;
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
        """)
        main_layout.addWidget(self.project_sidebar)
        
        # Main Content Area - Splitter for flexibility
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Center - Tab Widget (Chat, Editor, etc.)
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(False)
        self.tab_widget.setMovable(True)
        self.tab_widget.setDocumentMode(True)
        content_splitter.addWidget(self.tab_widget)
        
        # Right Sidebar - Can be used for additional panels (optional)
        # For now, we'll keep it simple and just use the main area
        
        main_layout.addWidget(content_splitter, 1)  # Stretch factor
        
        # Connect sidebar file selection to code editor
        self.project_sidebar.file_selected.connect(self._on_project_file_selected)
        
    def _create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        new_chat_action = QAction("&New Chat", self)
        new_chat_action.setShortcut(QKeySequence("Ctrl+N"))
        new_chat_action.triggered.connect(self._new_chat)
        file_menu.addAction(new_chat_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Agent menu
        agent_menu = menubar.addMenu("&Agent")
        
        simple_agent_action = QAction("&Simple Agent", self)
        simple_agent_action.setCheckable(True)
        simple_agent_action.setChecked(True)
        simple_agent_action.triggered.connect(lambda: self._set_agent_mode("simple"))
        agent_menu.addAction(simple_agent_action)
        
        expert_agent_action = QAction("&Expert Agent", self)
        expert_agent_action.setCheckable(True)
        expert_agent_action.triggered.connect(lambda: self._set_agent_mode("expert"))
        agent_menu.addAction(expert_agent_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        chat_action = QAction("&Chat", self)
        chat_action.setShortcut(QKeySequence("Ctrl+1"))
        chat_action.triggered.connect(lambda: self._switch_tab(0))
        view_menu.addAction(chat_action)
        
        files_action = QAction("&File Manager", self)
        files_action.setShortcut(QKeySequence("Ctrl+2"))
        files_action.triggered.connect(lambda: self._switch_tab(1))
        view_menu.addAction(files_action)
        
        editor_action = QAction("&Code Editor", self)
        editor_action.setShortcut(QKeySequence("Ctrl+3"))
        editor_action.triggered.connect(lambda: self._switch_tab(2))
        view_menu.addAction(editor_action)
        
        dashboard_action = QAction("&Dashboard", self)
        dashboard_action.setShortcut(QKeySequence("Ctrl+4"))
        dashboard_action.triggered.connect(lambda: self._switch_tab(3))
        view_menu.addAction(dashboard_action)
        
        settings_action = QAction("&Settings", self)
        settings_action.setShortcut(QKeySequence("Ctrl+,"))
        settings_action.triggered.connect(lambda: self._switch_tab(4))
        view_menu.addAction(settings_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
        
    def _create_toolbar(self):
        """Create toolbar with modern design"""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(20, 20))
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.addToolBar(toolbar)
        
        # New chat button
        new_chat_action = QAction("➕ New Chat", self)
        new_chat_action.setShortcut(QKeySequence("Ctrl+N"))
        new_chat_action.triggered.connect(self._new_chat)
        toolbar.addAction(new_chat_action)
        
        toolbar.addSeparator()
        
        # Agent mode toggle
        self.agent_mode_action = QAction("🤖 Simple Agent", self)
        self.agent_mode_action.setCheckable(True)
        self.agent_mode_action.setChecked(True)
        self.agent_mode_action.triggered.connect(self._toggle_agent_mode)
        toolbar.addAction(self.agent_mode_action)
        
    def _create_status_bar(self):
        """Create status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
    def _new_chat(self):
        """Create new chat session"""
        if self.chat_widget:
            self.chat_widget.new_chat()
            self.status_bar.showMessage("New chat session started", 3000)
    
    def _set_agent_mode(self, mode: str):
        """Set agent mode"""
        self.agent_mode_changed.emit(mode)
        self.agent_mode_action.setText(f"{mode.capitalize()} Agent")
        self.status_bar.showMessage(f"Switched to {mode.capitalize()} Agent", 3000)
    
    def _toggle_agent_mode(self):
        """Toggle between simple and expert agent"""
        current_mode = "expert" if self.agent_mode_action.isChecked() else "simple"
        self._set_agent_mode(current_mode)
    
    def _switch_tab(self, index: int):
        """Switch to specific tab"""
        if 0 <= index < self.tab_widget.count():
            self.tab_widget.setCurrentIndex(index)
    
    def _show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About Local AI Agent",
            """
            <h2>Local AI Agent Desktop Application</h2>
            <p>Version 1.0.0</p>
            <p>A powerful, self-improving AI agent that runs locally using Ollama.</p>
            <p><b>Features:</b></p>
            <ul>
                <li>Interactive Chat Interface</li>
                <li>File Manager</li>
                <li>Code Editor</li>
                <li>Dashboard & Statistics</li>
                <li>Settings & Configuration</li>
            </ul>
            <p>Built with PyQt6</p>
            """
        )
    
    def add_tab(self, widget: QWidget, title: str, icon: QIcon = None):
        """Add a tab to the tab widget"""
        index = self.tab_widget.addTab(widget, title)
        if icon:
            self.tab_widget.setTabIcon(index, icon)
        return index
    
    def set_chat_widget(self, widget):
        """Set chat widget reference"""
        self.chat_widget = widget
    
    def set_file_manager(self, widget):
        """Set file manager reference"""
        self.file_manager = widget
    
    def set_code_editor(self, widget):
        """Set code editor reference"""
        self.code_editor = widget
    
    def set_dashboard(self, widget):
        """Set dashboard reference"""
        self.dashboard = widget
    
    def set_settings(self, widget):
        """Set settings reference"""
        self.settings = widget
    
    def _on_project_file_selected(self, file_path: str):
        """Handle project file selection from sidebar"""
        if self.code_editor:
            self.code_editor._open_file_path(file_path)
            # Switch to editor tab
            for i in range(self.tab_widget.count()):
                if self.tab_widget.widget(i) == self.code_editor:
                    self.tab_widget.setCurrentIndex(i)
                    break
    
    def closeEvent(self, event):
        """Handle window close event"""
        reply = QMessageBox.question(
            self,
            "Exit Application",
            "Are you sure you want to exit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

