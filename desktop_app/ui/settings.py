"""
Settings Widget
لوحة الإعدادات
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QCheckBox,
    QSpinBox, QGroupBox, QFormLayout, QMessageBox,
    QFileDialog, QScrollArea, QTabWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
import json
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


class Settings(QWidget):
    """Settings widget"""
    
    settings_changed = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings_file = Path.home() / ".local_ai_agent" / "settings.json"
        self.settings_file.parent.mkdir(parents=True, exist_ok=True)
        self.settings = self._load_settings()
        self._init_ui()
    
    def _load_settings(self) -> dict:
        """Load settings from file"""
        default_settings = {
            "ollama_url": "http://localhost:11434",
            "default_model": "qwen2.5:3b",
            "max_iterations": 10,
            "auto_approve": False,
            "theme": "light",
            "font_size": 11,
            "enable_notifications": True,
            "save_history": True,
            "knowledge_base_path": "",
            "memory_db_path": ""
        }
        
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    loaded = json.load(f)
                    default_settings.update(loaded)
            except Exception as e:
                print(f"Error loading settings: {e}")
        
        return default_settings
    
    def _save_settings(self):
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {str(e)}")
            return False
    
    def _init_ui(self):
        """Initialize settings UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(15)
        
        # Tab widget for different setting categories
        tab_widget = QTabWidget()
        
        # Agent Settings
        agent_tab = self._create_agent_settings_tab()
        tab_widget.addTab(agent_tab, "Agent")
        
        # UI Settings
        ui_tab = self._create_ui_settings_tab()
        tab_widget.addTab(ui_tab, "UI")
        
        # Paths Settings
        paths_tab = self._create_paths_settings_tab()
        tab_widget.addTab(paths_tab, "Paths")
        
        # Advanced Settings
        advanced_tab = self._create_advanced_settings_tab()
        tab_widget.addTab(advanced_tab, "Advanced")
        
        content_layout.addWidget(tab_widget)
        content_layout.addStretch()
        
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_button = QPushButton("Save Settings")
        save_button.setStyleSheet("background-color: #28a745; color: white; padding: 8px 20px;")
        save_button.clicked.connect(self._on_save)
        
        reset_button = QPushButton("Reset to Defaults")
        reset_button.setStyleSheet("background-color: #dc3545; color: white; padding: 8px 20px;")
        reset_button.clicked.connect(self._on_reset)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(reset_button)
        
        layout.addLayout(button_layout)
    
    def _create_agent_settings_tab(self) -> QWidget:
        """Create agent settings tab"""
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(15)
        
        # Ollama URL
        self.ollama_url_edit = QLineEdit()
        self.ollama_url_edit.setText(self.settings.get("ollama_url", "http://localhost:11434"))
        layout.addRow("Ollama URL:", self.ollama_url_edit)
        
        # Default Model
        self.model_combo = QComboBox()
        self.model_combo.setEditable(True)
        self.model_combo.addItems([
            "qwen2.5:3b", "qwen2.5:7b", "qwen2.5:14b",
            "llama3.1:8b", "llama3.1:70b",
            "deepseek-coder:6.7b", "mistral:7b"
        ])
        self.model_combo.setCurrentText(self.settings.get("default_model", "qwen2.5:3b"))
        layout.addRow("Default Model:", self.model_combo)
        
        # Max Iterations
        self.max_iterations_spin = QSpinBox()
        self.max_iterations_spin.setMinimum(1)
        self.max_iterations_spin.setMaximum(50)
        self.max_iterations_spin.setValue(self.settings.get("max_iterations", 10))
        layout.addRow("Max Iterations:", self.max_iterations_spin)
        
        # Auto Approve
        self.auto_approve_check = QCheckBox()
        self.auto_approve_check.setChecked(self.settings.get("auto_approve", False))
        layout.addRow("Auto Approve Actions:", self.auto_approve_check)
        
        return widget
    
    def _create_ui_settings_tab(self) -> QWidget:
        """Create UI settings tab"""
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(15)
        
        # Theme
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["light", "dark"])
        self.theme_combo.setCurrentText(self.settings.get("theme", "light"))
        layout.addRow("Theme:", self.theme_combo)
        
        # Font Size
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setMinimum(8)
        self.font_size_spin.setMaximum(24)
        self.font_size_spin.setValue(self.settings.get("font_size", 11))
        layout.addRow("Font Size:", self.font_size_spin)
        
        # Enable Notifications
        self.notifications_check = QCheckBox()
        self.notifications_check.setChecked(self.settings.get("enable_notifications", True))
        layout.addRow("Enable Notifications:", self.notifications_check)
        
        # Save History
        self.save_history_check = QCheckBox()
        self.save_history_check.setChecked(self.settings.get("save_history", True))
        layout.addRow("Save Chat History:", self.save_history_check)
        
        return widget
    
    def _create_paths_settings_tab(self) -> QWidget:
        """Create paths settings tab"""
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(15)
        
        # Knowledge Base Path
        kb_layout = QHBoxLayout()
        self.kb_path_edit = QLineEdit()
        self.kb_path_edit.setText(self.settings.get("knowledge_base_path", ""))
        kb_browse_btn = QPushButton("Browse")
        kb_browse_btn.clicked.connect(lambda: self._browse_path(self.kb_path_edit, "Select Knowledge Base Directory"))
        kb_layout.addWidget(self.kb_path_edit)
        kb_layout.addWidget(kb_browse_btn)
        layout.addRow("Knowledge Base Path:", kb_layout)
        
        # Memory DB Path
        db_layout = QHBoxLayout()
        self.db_path_edit = QLineEdit()
        self.db_path_edit.setText(self.settings.get("memory_db_path", ""))
        db_browse_btn = QPushButton("Browse")
        db_browse_btn.clicked.connect(lambda: self._browse_file(self.db_path_edit, "Select Memory Database File", "*.db"))
        db_layout.addWidget(self.db_path_edit)
        db_layout.addWidget(db_browse_btn)
        layout.addRow("Memory DB Path:", db_layout)
        
        return widget
    
    def _create_advanced_settings_tab(self) -> QWidget:
        """Create advanced settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        info_label = QLabel(
            "Advanced settings and experimental features will be added here."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: gray; padding: 20px;")
        layout.addWidget(info_label)
        
        layout.addStretch()
        
        return widget
    
    def _browse_path(self, line_edit: QLineEdit, title: str):
        """Browse for directory"""
        directory = QFileDialog.getExistingDirectory(self, title)
        if directory:
            line_edit.setText(directory)
    
    def _browse_file(self, line_edit: QLineEdit, title: str, filter: str = ""):
        """Browse for file"""
        file_path, _ = QFileDialog.getOpenFileName(self, title, "", filter)
        if file_path:
            line_edit.setText(file_path)
    
    def _on_save(self):
        """Save settings"""
        # Update settings dict
        self.settings["ollama_url"] = self.ollama_url_edit.text()
        self.settings["default_model"] = self.model_combo.currentText()
        self.settings["max_iterations"] = self.max_iterations_spin.value()
        self.settings["auto_approve"] = self.auto_approve_check.isChecked()
        self.settings["theme"] = self.theme_combo.currentText()
        self.settings["font_size"] = self.font_size_spin.value()
        self.settings["enable_notifications"] = self.notifications_check.isChecked()
        self.settings["save_history"] = self.save_history_check.isChecked()
        self.settings["knowledge_base_path"] = self.kb_path_edit.text()
        self.settings["memory_db_path"] = self.db_path_edit.text()
        
        if self._save_settings():
            self.settings_changed.emit(self.settings)
            QMessageBox.information(self, "Success", "Settings saved successfully!")
    
    def _on_reset(self):
        """Reset settings to defaults"""
        reply = QMessageBox.question(
            self,
            "Reset Settings",
            "Are you sure you want to reset all settings to defaults?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.settings = self._load_settings()
            # Reload UI
            self._init_ui()
            QMessageBox.information(self, "Success", "Settings reset to defaults!")

