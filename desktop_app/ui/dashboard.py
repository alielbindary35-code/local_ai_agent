"""
Dashboard Widget - Statistics and Metrics
لوحة التحكم - الإحصائيات والمقاييس
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QProgressBar,
    QGroupBox, QGridLayout, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import sys
import os
from pathlib import Path
import psutil
import sqlite3

# Add project root to path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.paths import get_memory_db_file


class Dashboard(QWidget):
    """Dashboard widget showing statistics and metrics"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self._init_timer()
    
    def _init_ui(self):
        """Initialize dashboard UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Scroll area for dashboard content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(15)
        
        # System Resources Section
        system_group = self._create_system_resources_group()
        content_layout.addWidget(system_group)
        
        # Memory Statistics Section
        memory_group = self._create_memory_statistics_group()
        content_layout.addWidget(memory_group)
        
        # Knowledge Base Statistics Section
        kb_group = self._create_knowledge_base_group()
        content_layout.addWidget(kb_group)
        
        # Recent Activity Section
        activity_group = self._create_recent_activity_group()
        content_layout.addWidget(activity_group)
        
        content_layout.addStretch()
        
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
    
    def _create_system_resources_group(self) -> QGroupBox:
        """Create system resources group"""
        group = QGroupBox("System Resources")
        layout = QGridLayout()
        
        # CPU Usage
        self.cpu_label = QLabel("CPU Usage:")
        self.cpu_progress = QProgressBar()
        self.cpu_progress.setMaximum(100)
        self.cpu_value = QLabel("0%")
        layout.addWidget(self.cpu_label, 0, 0)
        layout.addWidget(self.cpu_progress, 0, 1)
        layout.addWidget(self.cpu_value, 0, 2)
        
        # Memory Usage
        self.memory_label = QLabel("Memory Usage:")
        self.memory_progress = QProgressBar()
        self.memory_progress.setMaximum(100)
        self.memory_value = QLabel("0%")
        layout.addWidget(self.memory_label, 1, 0)
        layout.addWidget(self.memory_progress, 1, 1)
        layout.addWidget(self.memory_value, 1, 2)
        
        # Disk Usage
        self.disk_label = QLabel("Disk Usage:")
        self.disk_progress = QProgressBar()
        self.disk_progress.setMaximum(100)
        self.disk_value = QLabel("0%")
        layout.addWidget(self.disk_label, 2, 0)
        layout.addWidget(self.disk_progress, 2, 1)
        layout.addWidget(self.disk_value, 2, 2)
        
        group.setLayout(layout)
        return group
    
    def _create_memory_statistics_group(self) -> QGroupBox:
        """Create memory statistics group"""
        group = QGroupBox("Memory Statistics")
        layout = QVBoxLayout()
        
        self.memory_table = QTableWidget()
        self.memory_table.setColumnCount(3)
        self.memory_table.setHorizontalHeaderLabels(["Metric", "Value", "Description"])
        self.memory_table.horizontalHeader().setStretchLastSection(True)
        self.memory_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.memory_table)
        
        group.setLayout(layout)
        return group
    
    def _create_knowledge_base_group(self) -> QGroupBox:
        """Create knowledge base statistics group"""
        group = QGroupBox("Knowledge Base Statistics")
        layout = QVBoxLayout()
        
        self.kb_table = QTableWidget()
        self.kb_table.setColumnCount(2)
        self.kb_table.setHorizontalHeaderLabels(["Category", "Count"])
        self.kb_table.horizontalHeader().setStretchLastSection(True)
        self.kb_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.kb_table)
        
        group.setLayout(layout)
        return group
    
    def _create_recent_activity_group(self) -> QGroupBox:
        """Create recent activity group"""
        group = QGroupBox("Recent Activity")
        layout = QVBoxLayout()
        
        self.activity_table = QTableWidget()
        self.activity_table.setColumnCount(3)
        self.activity_table.setHorizontalHeaderLabels(["Time", "Type", "Description"])
        self.activity_table.horizontalHeader().setStretchLastSection(True)
        self.activity_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.activity_table)
        
        group.setLayout(layout)
        return group
    
    def _init_timer(self):
        """Initialize update timer"""
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_all)
        self.timer.start(2000)  # Update every 2 seconds
        self._update_all()  # Initial update
    
    def _update_all(self):
        """Update all dashboard metrics"""
        self._update_system_resources()
        self._update_memory_statistics()
        self._update_knowledge_base_statistics()
        self._update_recent_activity()
    
    def _update_system_resources(self):
        """Update system resources"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=0.1)
            self.cpu_progress.setValue(int(cpu_percent))
            self.cpu_value.setText(f"{cpu_percent:.1f}%")
            
            # Memory
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            self.memory_progress.setValue(int(memory_percent))
            self.memory_value.setText(f"{memory_percent:.1f}% ({memory.used / 1024**3:.2f} GB / {memory.total / 1024**3:.2f} GB)")
            
            # Disk (handle Windows vs Unix paths)
            try:
                if sys.platform == 'win32':
                    disk = psutil.disk_usage('C:\\')
                else:
                    disk = psutil.disk_usage('/')
                disk_percent = disk.percent
                self.disk_progress.setValue(int(disk_percent))
                self.disk_value.setText(f"{disk_percent:.1f}% ({disk.used / 1024**3:.2f} GB / {disk.total / 1024**3:.2f} GB)")
            except Exception:
                self.disk_progress.setValue(0)
                self.disk_value.setText("N/A")
        except Exception as e:
            print(f"Error updating system resources: {e}")
    
    def _update_memory_statistics(self):
        """Update memory statistics from database"""
        try:
            db_path = get_memory_db_file()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get solutions count
            cursor.execute("SELECT COUNT(*) FROM solutions")
            solutions_count = cursor.fetchone()[0]
            
            # Get custom tools count
            cursor.execute("SELECT COUNT(*) FROM custom_tools")
            tools_count = cursor.fetchone()[0]
            
            # Get packages count
            cursor.execute("SELECT COUNT(*) FROM packages")
            packages_count = cursor.fetchone()[0]
            
            # Get errors count
            cursor.execute("SELECT COUNT(*) FROM errors")
            errors_count = cursor.fetchone()[0]
            
            # Get average rating
            cursor.execute("SELECT AVG(rating) FROM solutions WHERE rating > 0")
            avg_rating = cursor.fetchone()[0] or 0
            
            conn.close()
            
            # Update table
            self.memory_table.setRowCount(5)
            
            data = [
                ("Solutions Stored", str(solutions_count), "Total number of saved solutions"),
                ("Custom Tools", str(tools_count), "Number of custom tools registered"),
                ("Packages Tracked", str(packages_count), "Number of packages installed"),
                ("Errors Recorded", str(errors_count), "Number of errors encountered"),
                ("Average Rating", f"{avg_rating:.2f}", "Average solution rating")
            ]
            
            for row, (metric, value, desc) in enumerate(data):
                self.memory_table.setItem(row, 0, QTableWidgetItem(metric))
                self.memory_table.setItem(row, 1, QTableWidgetItem(value))
                self.memory_table.setItem(row, 2, QTableWidgetItem(desc))
            
            self.memory_table.resizeColumnsToContents()
        except Exception as e:
            print(f"Error updating memory statistics: {e}")
    
    def _update_knowledge_base_statistics(self):
        """Update knowledge base statistics"""
        try:
            db_path = get_memory_db_file()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get knowledge entries by category
            cursor.execute("""
                SELECT category, COUNT(*) 
                FROM knowledge_entries 
                GROUP BY category
                ORDER BY COUNT(*) DESC
            """)
            
            categories = cursor.fetchall()
            conn.close()
            
            # Update table
            self.kb_table.setRowCount(len(categories))
            
            for row, (category, count) in enumerate(categories):
                self.kb_table.setItem(row, 0, QTableWidgetItem(category or "Uncategorized"))
                self.kb_table.setItem(row, 1, QTableWidgetItem(str(count)))
            
            self.kb_table.resizeColumnsToContents()
        except Exception as e:
            print(f"Error updating knowledge base statistics: {e}")
    
    def _update_recent_activity(self):
        """Update recent activity"""
        try:
            db_path = get_memory_db_file()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get recent solutions
            cursor.execute("""
                SELECT timestamp, problem, solution 
                FROM solutions 
                ORDER BY timestamp DESC 
                LIMIT 10
            """)
            
            activities = cursor.fetchall()
            conn.close()
            
            # Update table
            self.activity_table.setRowCount(len(activities))
            
            for row, (timestamp, problem, solution) in enumerate(activities):
                self.activity_table.setItem(row, 0, QTableWidgetItem(timestamp[:19] if timestamp else ""))
                self.activity_table.setItem(row, 1, QTableWidgetItem("Solution"))
                desc = problem[:50] + "..." if len(problem) > 50 else problem
                self.activity_table.setItem(row, 2, QTableWidgetItem(desc))
            
            self.activity_table.resizeColumnsToContents()
        except Exception as e:
            print(f"Error updating recent activity: {e}")

