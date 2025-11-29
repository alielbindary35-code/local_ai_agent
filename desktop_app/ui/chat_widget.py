"""
Chat Widget - Main chat interface
واجهة المحادثة الرئيسية
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QPushButton, QScrollArea, QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QKeyEvent

from desktop_app.widgets.message_bubble import MessageBubble
from desktop_app.core.agent_bridge import AgentBridge


class ChatWidget(QWidget):
    """Main chat interface widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.messages = []
        self._init_ui()
        self._init_agent_bridge()
    
    def _init_ui(self):
        """Initialize the chat UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Chat history area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #ffffff;
            }
        """)
        
        self.chat_container = QWidget()
        self.chat_container.setStyleSheet("background-color: #ffffff;")
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_layout.setSpacing(16)
        self.chat_layout.setContentsMargins(20, 20, 20, 20)
        self.chat_layout.addStretch()
        
        self.scroll_area.setWidget(self.chat_container)
        layout.addWidget(self.scroll_area)
        
        # Input area
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Type your message here... (Press Ctrl+Enter to send)")
        self.input_field.setMaximumHeight(100)
        # Font will be set via stylesheet
        self.input_field.setStyleSheet("""
            QTextEdit {
                border: 1px solid #d1d5db;
                border-radius: 12px;
                padding: 12px 16px;
                background-color: #ffffff;
                font-family: 'Inter', 'Segoe UI', -apple-system, sans-serif;
                font-size: 14px;
                color: #1f2937;
            }
            QTextEdit:focus {
                border: 2px solid #3b82f6;
                background-color: #ffffff;
            }
        """)
        self.input_field.keyPressEvent = self._handle_key_press
        
        self.send_button = QPushButton("Send")
        self.send_button.setMinimumWidth(100)
        self.send_button.setMinimumHeight(40)
        self.send_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:1 #2563eb);
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: 600;
                font-size: 14px;
                padding: 12px 24px;
                min-width: 100px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2563eb, stop:1 #1d4ed8);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1d4ed8, stop:1 #1e40af);
            }
            QPushButton:disabled {
                background-color: #e5e7eb;
                color: #9ca3af;
            }
        """)
        self.send_button.clicked.connect(self._send_message)
        
        input_layout.addWidget(self.input_field, 4)
        input_layout.addWidget(self.send_button, 1)
        
        layout.addLayout(input_layout)
        
        # Status label - modern design
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
    
    def _init_agent_bridge(self):
        """Initialize agent bridge"""
        self.agent_bridge = AgentBridge(self, enable_streaming=True)
        self.agent_bridge.response_received.connect(self._on_response_received)
        self.agent_bridge.response_chunk.connect(self._on_response_chunk)
        self.agent_bridge.error_occurred.connect(self._on_error_occurred)
        self.agent_bridge.thinking.connect(self._on_thinking)
        self.current_response_bubble = None
        self.current_response_text = ""
    
    def _handle_key_press(self, event: QKeyEvent):
        """Handle key press in input field"""
        if event.key() == Qt.Key.Key_Return and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self._send_message()
        else:
            # Call original keyPressEvent
            QTextEdit.keyPressEvent(self.input_field, event)
    
    def _send_message(self):
        """Send message to agent"""
        user_input = self.input_field.toPlainText().strip()
        if not user_input:
            return
        
        # Add user message to chat
        self._add_message(user_input, is_user=True)
        
        # Clear input
        self.input_field.clear()
        
        # Reset streaming state
        self.current_response_bubble = None
        self.current_response_text = ""
        
        # Send to agent
        self.status_label.setText("Processing...")
        self.send_button.setEnabled(False)
        self.agent_bridge.send_message(user_input)
    
    def _add_message(self, message: str, is_user: bool = True):
        """Add message bubble to chat"""
        bubble = MessageBubble(message, is_user=is_user)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)
        self.messages.append({"message": message, "is_user": is_user})
        
        # Scroll to bottom
        QWidget.scroll_area = self.scroll_area
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )
    
    def _on_response_chunk(self, chunk: str):
        """Handle streaming response chunk"""
        if self.current_response_bubble is None:
            # Create new bubble for streaming
            self.current_response_text = ""
            self.current_response_bubble = MessageBubble("", is_user=False)
            self.chat_layout.insertWidget(self.chat_layout.count() - 1, self.current_response_bubble)
        
        # Append chunk
        self.current_response_text += chunk
        self.current_response_bubble.message = self.current_response_text
        self.current_response_bubble.message_label.setHtml(
            self.current_response_bubble._markdown_to_html(self.current_response_text)
        )
        
        # Scroll to bottom
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )
    
    def _on_response_received(self, response: str):
        """Handle agent response"""
        # Clean response - remove any console formatting artifacts
        if response:
            # Remove any ANSI codes or console formatting
            import re
            # Remove ANSI escape sequences
            ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
            response = ansi_escape.sub('', response)
            # Remove any console panel markers
            response = response.strip()
        
        if self.current_response_bubble:
            # Update existing streaming bubble
            self.current_response_bubble.message = response
            self.current_response_bubble.message_label.setHtml(
                self.current_response_bubble._markdown_to_html(response)
            )
            self.current_response_bubble = None
        else:
            # Add new message if streaming wasn't used
            if response:
                self._add_message(response, is_user=False)
        
        self.status_label.setText("Ready")
        self.send_button.setEnabled(True)
        self.current_response_text = ""
    
    def _on_error_occurred(self, error: str):
        """Handle agent error"""
        self._add_message(f"❌ Error: {error}", is_user=False)
        self.status_label.setText(f"Error: {error}")
        self.send_button.setEnabled(True)
    
    def _on_thinking(self, message: str):
        """Handle thinking status"""
        self.status_label.setText(message)
    
    def new_chat(self):
        """Start new chat session"""
        # Clear messages
        while self.chat_layout.count() > 1:  # Keep the stretch
            item = self.chat_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.messages.clear()
        self.status_label.setText("New chat started")
    
    def set_agent_mode(self, mode: str):
        """Set agent mode"""
        self.agent_bridge.set_agent_mode(mode)
        self.status_label.setText(f"Switched to {mode.capitalize()} Agent")

