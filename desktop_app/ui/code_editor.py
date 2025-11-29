"""
Code Editor Widget
محرر الكود
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QLabel, QFileDialog, QMessageBox, QTextEdit
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QTextCharFormat, QColor, QSyntaxHighlighter, QTextDocument
from pathlib import Path
import re


class PythonHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for Python code"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_rules()
    
    def _init_rules(self):
        """Initialize highlighting rules"""
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#0000FF"))
        keyword_format.setFontWeight(700)
        
        keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'exec', 'finally', 'for',
            'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
            'not', 'or', 'pass', 'print', 'raise', 'return', 'try',
            'while', 'with', 'yield', 'True', 'False', 'None'
        ]
        
        self.rules = []
        for keyword in keywords:
            pattern = r'\b' + keyword + r'\b'
            self.rules.append((pattern, keyword_format))
        
        # String formatting
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#008000"))
        self.rules.append((r'"[^"]*"', string_format))
        self.rules.append((r"'[^']*'", string_format))
        
        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#808080"))
        comment_format.setFontItalic(True)
        self.rules.append((r'#.*', comment_format))
        
        # Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#FF0000"))
        self.rules.append((r'\b\d+\b', number_format))
    
    def highlightBlock(self, text):
        """Apply highlighting to a block of text"""
        for pattern, format in self.rules:
            expression = re.compile(pattern)
            for match in expression.finditer(text):
                start, end = match.span()
                self.setFormat(start, end - start, format)


class CodeEditorTab(QTextEdit):
    """Single code editor tab"""
    
    def __init__(self, file_path: str = None, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.is_modified = False
        
        # Set font
        font = QFont("Consolas")
        font.setPointSize(11)
        font.setFixedPitch(True)
        self.setFont(font)
        
        # Set tab width
        self.setTabStopDistance(40)
        
        # Add syntax highlighter
        self.highlighter = PythonHighlighter(self.document())
        
        # Load file if provided
        if file_path:
            self.load_file(file_path)
        
        # Track modifications
        self.textChanged.connect(self._on_text_changed)
    
    def _on_text_changed(self):
        """Handle text changes"""
        self.is_modified = True
    
    def load_file(self, file_path: str):
        """Load file into editor"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.setPlainText(content)
                self.file_path = file_path
                self.is_modified = False
                return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")
            return False
    
    def save_file(self, file_path: str = None):
        """Save file"""
        if file_path:
            self.file_path = file_path
        
        if not self.file_path:
            return False
        
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(self.toPlainText())
                self.is_modified = False
                return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
            return False
    
    def get_title(self) -> str:
        """Get tab title"""
        if self.file_path:
            name = Path(self.file_path).name
            if self.is_modified:
                return f"{name} *"
            return name
        return "Untitled *" if self.is_modified else "Untitled"


class CodeEditor(QWidget):
    """Code editor widget with tabs"""
    
    file_opened = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """Initialize code editor UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Toolbar
        toolbar_layout = QHBoxLayout()
        
        new_button = QPushButton("New")
        new_button.clicked.connect(self._new_file)
        
        open_button = QPushButton("Open")
        open_button.clicked.connect(self._open_file)
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self._save_file)
        
        save_as_button = QPushButton("Save As")
        save_as_button.clicked.connect(self._save_as_file)
        
        run_button = QPushButton("Run")
        run_button.setStyleSheet("background-color: #28a745; color: white;")
        run_button.clicked.connect(self._run_code)
        
        toolbar_layout.addWidget(new_button)
        toolbar_layout.addWidget(open_button)
        toolbar_layout.addWidget(save_button)
        toolbar_layout.addWidget(save_as_button)
        toolbar_layout.addSpacing(20)  # Spacer instead of separator
        toolbar_layout.addWidget(run_button)
        toolbar_layout.addStretch()
        
        layout.addLayout(toolbar_layout)
        
        # Tab widget for multiple files
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self._close_tab)
        self.tab_widget.currentChanged.connect(self._on_tab_changed)
        
        layout.addWidget(self.tab_widget)
        
        # Status - modern design
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("""
            color: #6b7280; 
            font-size: 12px; 
            padding: 8px 12px;
            background-color: #f9fafb;
            border-radius: 6px;
            font-weight: 500;
        """)
        layout.addWidget(self.status_label)
        
        # Create initial untitled tab
        self._new_file()
    
    def _new_file(self):
        """Create new file tab"""
        editor = CodeEditorTab()
        index = self.tab_widget.addTab(editor, editor.get_title())
        self.tab_widget.setCurrentIndex(index)
        self.status_label.setText("New file created")
    
    def _open_file(self):
        """Open file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            str(Path.cwd()),
            "All Files (*);;Python Files (*.py);;Text Files (*.txt);;Markdown Files (*.md)"
        )
        
        if file_path:
            self._open_file_path(file_path)
    
    def _open_file_path(self, file_path: str):
        """Open file at specific path"""
        # Check if file is already open
        for i in range(self.tab_widget.count()):
            editor = self.tab_widget.widget(i)
            if hasattr(editor, 'file_path') and editor.file_path == file_path:
                self.tab_widget.setCurrentIndex(i)
                self.status_label.setText(f"File already open: {file_path}")
                return
        
        # Open new tab
        try:
            editor = CodeEditorTab(file_path)
            index = self.tab_widget.addTab(editor, editor.get_title())
            self.tab_widget.setCurrentIndex(index)
            self.file_opened.emit(file_path)
            self.status_label.setText(f"Opened: {file_path}")
        except Exception as e:
            self.status_label.setText(f"Error opening file: {str(e)}")
    
    def _save_file(self):
        """Save current file"""
        editor = self._get_current_editor()
        if not editor:
            return
        
        if editor.file_path:
            if editor.save_file():
                self._update_tab_title()
                self.status_label.setText(f"Saved: {editor.file_path}")
        else:
            self._save_as_file()
    
    def _save_as_file(self):
        """Save file as"""
        editor = self._get_current_editor()
        if not editor:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            str(Path.cwd()),
            "All Files (*);;Python Files (*.py);;Text Files (*.txt);;Markdown Files (*.md)"
        )
        
        if file_path:
            if editor.save_file(file_path):
                self._update_tab_title()
                self.status_label.setText(f"Saved: {file_path}")
    
    def _close_tab(self, index: int):
        """Close tab"""
        editor = self.tab_widget.widget(index)
        if editor and editor.is_modified:
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                f"File '{editor.get_title()}' has unsaved changes. Save before closing?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Yes
            )
            
            if reply == QMessageBox.StandardButton.Cancel:
                return
            elif reply == QMessageBox.StandardButton.Yes:
                if not editor.file_path:
                    file_path, _ = QFileDialog.getSaveFileName(self, "Save File")
                    if not file_path:
                        return
                    editor.file_path = file_path
                editor.save_file()
        
        self.tab_widget.removeTab(index)
        
        # Create new tab if no tabs left
        if self.tab_widget.count() == 0:
            self._new_file()
    
    def _run_code(self):
        """Run current code"""
        editor = self._get_current_editor()
        if not editor:
            return
        
        code = editor.toPlainText()
        if not code.strip():
            QMessageBox.warning(self, "Empty Code", "No code to run")
            return
        
        # Save file first if it has a path
        if editor.file_path:
            editor.save_file()
        
        # Execute code (basic implementation)
        # Note: In production, use a safer execution environment
        try:
            # Create a safe execution namespace
            namespace = {'__builtins__': __builtins__}
            exec(code, namespace)
            self.status_label.setText("Code executed successfully")
            QMessageBox.information(self, "Success", "Code executed successfully")
        except Exception as e:
            import traceback
            error_msg = f"Error: {str(e)}\n\n{traceback.format_exc()}"
            self.status_label.setText(f"Error: {str(e)}")
            QMessageBox.critical(self, "Execution Error", error_msg)
    
    def _get_current_editor(self) -> CodeEditorTab:
        """Get current editor tab"""
        return self.tab_widget.currentWidget()
    
    def _update_tab_title(self):
        """Update current tab title"""
        editor = self._get_current_editor()
        if editor:
            index = self.tab_widget.currentIndex()
            self.tab_widget.setTabText(index, editor.get_title())
    
    def _on_tab_changed(self, index: int):
        """Handle tab change"""
        editor = self.tab_widget.widget(index)
        if editor:
            if editor.file_path:
                self.status_label.setText(f"Current file: {editor.file_path}")
            else:
                self.status_label.setText("Untitled file")

