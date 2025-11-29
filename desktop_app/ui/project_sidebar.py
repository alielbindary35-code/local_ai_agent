"""
Project Sidebar - Left sidebar for project files
الشريط الجانبي للمشروع
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeView,
    QLabel, QPushButton, QLineEdit
)
from PyQt6.QtCore import Qt, QDir, QModelIndex, pyqtSignal
from PyQt6.QtGui import QFileSystemModel
from pathlib import Path
import os


class ProjectSidebar(QWidget):
    """Project sidebar widget - shows project files"""
    
    file_selected = pyqtSignal(str)  # Signal when file is selected
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """Initialize sidebar UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(12, 12, 12, 12)
        
        title_label = QLabel("📁 Project")
        title_label.setStyleSheet("""
            font-weight: 600;
            font-size: 13px;
            color: #1f2937;
            padding: 4px;
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Search box
        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(12, 0, 12, 12)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search files...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                padding: 6px 10px;
                background-color: #ffffff;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 1px solid #3b82f6;
            }
        """)
        search_layout.addWidget(self.search_input)
        
        layout.addLayout(search_layout)
        
        # File tree
        self.tree_view = QTreeView()
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setRootIsDecorated(True)
        self.tree_view.setAnimated(True)
        self.tree_view.setIndentation(15)
        
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.rootPath())
        self.tree_view.setModel(self.file_model)
        
        # Set root to current project directory
        project_root = Path.cwd()
        index = self.file_model.index(str(project_root))
        self.tree_view.setRootIndex(index)
        self.tree_view.setColumnWidth(0, 200)
        
        # Hide columns except name
        self.tree_view.hideColumn(1)
        self.tree_view.hideColumn(2)
        self.tree_view.hideColumn(3)
        
        self.tree_view.clicked.connect(self._on_file_clicked)
        self.tree_view.doubleClicked.connect(self._on_file_double_clicked)
        
        layout.addWidget(self.tree_view)
        
        # Footer with project info
        footer = QLabel(f"📂 {Path.cwd().name}")
        footer.setStyleSheet("""
            color: #6b7280;
            font-size: 11px;
            padding: 8px 12px;
            background-color: #f9fafb;
            border-top: 1px solid #e5e7eb;
        """)
        layout.addWidget(footer)
    
    def _on_file_clicked(self, index: QModelIndex):
        """Handle file click"""
        file_path = self.file_model.filePath(index)
        if os.path.isfile(file_path):
            self.file_selected.emit(file_path)
    
    def _on_file_double_clicked(self, index: QModelIndex):
        """Handle file double-click"""
        file_path = self.file_model.filePath(index)
        if os.path.isfile(file_path):
            self.file_selected.emit(file_path)

