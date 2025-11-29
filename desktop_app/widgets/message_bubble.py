"""
Message Bubble Widget for Chat Interface
عنصر رسالة المحادثة
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QPalette, QFont
import markdown
from datetime import datetime


class MessageBubble(QWidget):
    """A single message bubble in the chat"""
    
    def __init__(self, message: str, is_user: bool = True, timestamp: str = None, parent=None):
        super().__init__(parent)
        self.message = message
        self.is_user = is_user
        self.timestamp = timestamp or datetime.now().strftime("%H:%M")
        
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the message bubble UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
        # Create message container
        message_container = QWidget()
        message_layout = QVBoxLayout(message_container)
        message_layout.setContentsMargins(12, 8, 12, 8)
        message_layout.setSpacing(4)
        
        # Message text
        self.message_label = QTextEdit()
        self.message_label.setReadOnly(True)
        self.message_label.setMaximumHeight(300)
        self.message_label.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.message_label.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Convert markdown to HTML
        html_content = self._markdown_to_html(self.message)
        self.message_label.setHtml(html_content)
        
        # Timestamp
        timestamp_label = QLabel(self.timestamp)
        if self.is_user:
            timestamp_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 11px; padding-top: 4px;")
        else:
            timestamp_label.setStyleSheet("color: #9ca3af; font-size: 11px; padding-top: 4px;")
        
        # Set colors based on message type - Modern Design
        if self.is_user:
            # User message - right aligned, modern blue gradient
            message_container.setStyleSheet("""
                QWidget {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #3b82f6, stop:1 #2563eb);
                    border-radius: 18px;
                    color: white;
                    padding: 0px;
                }
            """)
            self.message_label.setStyleSheet("""
                QTextEdit {
                    background-color: transparent;
                    border: none;
                    color: white;
                    font-size: 14px;
                    font-family: 'Inter', 'Segoe UI', -apple-system, sans-serif;
                    padding: 12px 16px;
                    line-height: 1.5;
                }
            """)
            layout.addStretch()
            layout.addWidget(message_container)
        else:
            # Agent message - left aligned, modern white card
            message_container.setStyleSheet("""
                QWidget {
                    background-color: #ffffff;
                    border-radius: 18px;
                    color: #1f2937;
                    border: 1px solid #e5e7eb;
                    padding: 0px;
                }
            """)
            self.message_label.setStyleSheet("""
                QTextEdit {
                    background-color: transparent;
                    border: none;
                    color: #1f2937;
                    font-size: 14px;
                    font-family: 'Inter', 'Segoe UI', -apple-system, sans-serif;
                    padding: 12px 16px;
                    line-height: 1.5;
                }
            """)
            layout.addWidget(message_container)
            layout.addStretch()
        
        message_layout.addWidget(self.message_label)
        message_layout.addWidget(timestamp_label)
        
        # Set fixed width for better appearance - wider for modern design
        self.setMaximumWidth(900)
    
    def _markdown_to_html(self, text: str) -> str:
        """Convert markdown text to HTML"""
        try:
            html = markdown.markdown(
                text,
                extensions=['codehilite', 'fenced_code', 'tables']
            )
            # Add some basic styling
            html = f"""
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; }}
                code {{ background-color: rgba(0,0,0,0.1); padding: 2px 4px; border-radius: 3px; }}
                pre {{ background-color: rgba(0,0,0,0.1); padding: 8px; border-radius: 4px; overflow-x: auto; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: rgba(0,0,0,0.1); }}
            </style>
            {html}
            """
            return html
        except Exception:
            # Fallback to plain text
            return f"<p>{text.replace(chr(10), '<br>')}</p>"
    
    def sizeHint(self):
        """Return preferred size"""
        return QSize(800, 100)

