"""
File Manager Widget
مدير الملفات
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeView,
    QTextEdit, QPushButton, QSplitter,
    QLabel, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt, QDir, QModelIndex
from PyQt6.QtGui import QIcon, QFileSystemModel, QFont
from pathlib import Path
import os


class FileManager(QWidget):
    """File manager widget with tree view and preview"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_file = None
        self._init_ui()
    
    def _init_ui(self):
        """Initialize file manager UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Toolbar
        toolbar_layout = QHBoxLayout()
        
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("Enter path or click Browse...")
        self.path_edit.returnPressed.connect(self._navigate_to_path)
        
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self._browse_directory)
        
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self._refresh_view)
        
        toolbar_layout.addWidget(QLabel("Path:"))
        toolbar_layout.addWidget(self.path_edit, 3)
        toolbar_layout.addWidget(browse_button)
        toolbar_layout.addWidget(refresh_button)
        
        layout.addLayout(toolbar_layout)
        
        # Splitter for tree and preview
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # File tree
        self.tree_view = QTreeView()
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.rootPath())
        self.tree_view.setModel(self.file_model)
        self.tree_view.setRootIndex(self.file_model.index(str(Path.cwd())))
        self.tree_view.setColumnWidth(0, 250)
        self.tree_view.doubleClicked.connect(self._on_file_selected)
        self.tree_view.clicked.connect(self._on_file_clicked)
        
        splitter.addWidget(self.tree_view)
        
        # Preview area
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)
        preview_layout.setContentsMargins(5, 5, 5, 5)
        
        preview_label = QLabel("File Preview")
        preview_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        preview_layout.addWidget(preview_label)
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        # Font will be set via stylesheet
        preview_font = QFont("Consolas")
        preview_font.setPointSize(10)
        self.preview_text.setFont(preview_font)
        preview_layout.addWidget(self.preview_text)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        self.open_button = QPushButton("Open in Editor")
        self.open_button.setEnabled(False)
        self.open_button.clicked.connect(self._open_in_editor)
        
        self.delete_button = QPushButton("Delete")
        self.delete_button.setEnabled(False)
        self.delete_button.setStyleSheet("background-color: #dc3545; color: white;")
        self.delete_button.clicked.connect(self._delete_file)
        
        action_layout.addWidget(self.open_button)
        action_layout.addWidget(self.delete_button)
        action_layout.addStretch()
        
        preview_layout.addLayout(action_layout)
        
        splitter.addWidget(preview_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        layout.addWidget(splitter)
        
        # Status - modern design
        self.status_label = QLabel(f"Current directory: {Path.cwd()}")
        self.status_label.setStyleSheet("""
            color: #6b7280; 
            font-size: 12px; 
            padding: 8px 12px;
            background-color: #f9fafb;
            border-radius: 6px;
            font-weight: 500;
        """)
        layout.addWidget(self.status_label)
    
    def _navigate_to_path(self):
        """Navigate to path entered in path edit"""
        path = self.path_edit.text().strip()
        if path and os.path.exists(path):
            index = self.file_model.index(path)
            if index.isValid():
                self.tree_view.setRootIndex(index)
                self.status_label.setText(f"Current directory: {path}")
            else:
                QMessageBox.warning(self, "Invalid Path", f"Path is not valid: {path}")
        else:
            QMessageBox.warning(self, "Path Not Found", f"Path does not exist: {path}")
    
    def _browse_directory(self):
        """Browse for directory"""
        from PyQt6.QtWidgets import QFileDialog
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Directory",
            str(Path.cwd())
        )
        if directory:
            self.path_edit.setText(directory)
            index = self.file_model.index(directory)
            self.tree_view.setRootIndex(index)
            self.status_label.setText(f"Current directory: {directory}")
    
    def _refresh_view(self):
        """Refresh file tree view"""
        current_index = self.tree_view.rootIndex()
        if current_index.isValid():
            path = self.file_model.filePath(current_index)
            self.file_model.setRootPath(path)
            self.tree_view.setRootIndex(self.file_model.index(path))
    
    def _on_file_clicked(self, index: QModelIndex):
        """Handle file click"""
        file_path = self.file_model.filePath(index)
        if os.path.isfile(file_path):
            self._preview_file(file_path)
            self.current_file = file_path
            self.open_button.setEnabled(True)
            self.delete_button.setEnabled(True)
        else:
            self.preview_text.clear()
            self.current_file = None
            self.open_button.setEnabled(False)
            self.delete_button.setEnabled(False)
    
    def _on_file_selected(self, index: QModelIndex):
        """Handle file double-click"""
        file_path = self.file_model.filePath(index)
        if os.path.isfile(file_path):
            self._open_in_editor(file_path)
        elif os.path.isdir(file_path):
            self.tree_view.setRootIndex(index)
            self.path_edit.setText(file_path)
            self.status_label.setText(f"Current directory: {file_path}")
    
    def _preview_file(self, file_path: str):
        """Preview file content"""
        try:
            # Check file size (preview only small files)
            file_size = os.path.getsize(file_path)
            if file_size > 1024 * 1024:  # 1MB limit
                self.preview_text.setText(f"File too large to preview ({file_size / 1024 / 1024:.2f} MB)")
                return
            
            # Try to read as text
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                self.preview_text.setPlainText(content)
        except Exception as e:
            self.preview_text.setText(f"Error reading file: {str(e)}")
    
    def _open_in_editor(self, file_path: str = None):
        """Open file in code editor"""
        if file_path is None:
            file_path = self.current_file
        
        if file_path and os.path.isfile(file_path):
            # Emit signal to open in editor (will be handled by main window)
            # For now, just show message
            QMessageBox.information(
                self,
                "Open in Editor",
                f"File will be opened in editor: {file_path}\n\n(This feature will be connected to Code Editor)"
            )
    
    def _delete_file(self):
        """Delete selected file"""
        if not self.current_file:
            return
        
        reply = QMessageBox.question(
            self,
            "Delete File",
            f"Are you sure you want to delete:\n{self.current_file}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                os.remove(self.current_file)
                self.preview_text.clear()
                self.current_file = None
                self.open_button.setEnabled(False)
                self.delete_button.setEnabled(False)
                self._refresh_view()
                QMessageBox.information(self, "Success", "File deleted successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete file: {str(e)}")

