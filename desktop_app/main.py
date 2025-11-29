"""
Main entry point for Desktop Application
نقطة الدخول الرئيسية لتطبيق سطح المكتب
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from desktop_app.ui.main_window import MainWindow
from desktop_app.styles_cursor import CURSOR_LIGHT_THEME
from desktop_app.ui.chat_widget import ChatWidget
from desktop_app.ui.file_manager import FileManager
from desktop_app.ui.code_editor import CodeEditor
from desktop_app.ui.dashboard import Dashboard
from desktop_app.ui.settings import Settings


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Local AI Agent")
    app.setOrganizationName("Local AI Agent")
    
    # Apply Cursor-inspired modern theme
    app.setStyleSheet(CURSOR_LIGHT_THEME)
    
    # Create main window
    main_window = MainWindow()
    
    # Create and add widgets
    chat_widget = ChatWidget()
    main_window.add_tab(chat_widget, "💬 Chat")
    main_window.set_chat_widget(chat_widget)
    
    file_manager = FileManager()
    main_window.add_tab(file_manager, "📁 Files")
    main_window.set_file_manager(file_manager)
    
    code_editor = CodeEditor()
    main_window.add_tab(code_editor, "📝 Editor")
    main_window.set_code_editor(code_editor)
    
    dashboard = Dashboard()
    main_window.add_tab(dashboard, "📊 Dashboard")
    main_window.set_dashboard(dashboard)
    
    settings = Settings()
    main_window.add_tab(settings, "⚙️ Settings")
    main_window.set_settings(settings)
    
    # Connect agent mode changes
    main_window.agent_mode_changed.connect(chat_widget.set_agent_mode)
    
    # Show window
    main_window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

