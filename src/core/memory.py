"""
Memory System - Persistent learning and knowledge storage
نظام الذاكرة - التعلم المستمر وتخزين المعرفة

SQLite-based memory system that stores solutions, custom tools,
package registry, and user preferences.
"""

import sqlite3
from datetime import datetime
from typing import List, Tuple, Dict, Any, Optional
from pathlib import Path

# Import paths system
from src.core.paths import get_memory_db_file


class Memory:
    """
    Advanced learning and memory system for the AI agent.
    
    نظام التعلم والذاكرة المتقدم لوكيل الذكاء الاصطناعي.
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize memory system.
        
        Args:
            db_path: Path to SQLite database file (defaults to centralized path)
        """
        if db_path is None:
            db_path = get_memory_db_file()
        self.db_path = str(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()
    
    def create_tables(self):
        """
        Create database tables if they don't exist.
        إنشاء جداول قاعدة البيانات إذا لم تكن موجودة.
        """
        cursor = self.conn.cursor()
        
        # Solutions table - جدول الحلول
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS solutions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                problem TEXT NOT NULL,
                solution TEXT NOT NULL,
                rating INTEGER DEFAULT 5,
                success_count INTEGER DEFAULT 0,
                timestamp TEXT NOT NULL,
                category TEXT,
                tags TEXT
            )
        """)
        
        # Custom tools table - جدول الأدوات المخصصة
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS custom_tools (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                command TEXT NOT NULL,
                description TEXT,
                usage_count INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)
        
        # Package registry - سجل الحزم
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                package_name TEXT UNIQUE NOT NULL,
                package_manager TEXT NOT NULL,
                reason TEXT,
                installed_at TEXT NOT NULL
            )
        """)
        
        # User preferences - تفضيلات المستخدم
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS preferences (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        # Error patterns - أنماط الأخطاء
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                error_message TEXT NOT NULL,
                solution TEXT,
                occurrence_count INTEGER DEFAULT 1,
                first_seen TEXT NOT NULL,
                last_seen TEXT NOT NULL
            )
        """)
        
        self.conn.commit()
    
    # ═══════════════════════════════════════════════════════════
    # SOLUTIONS MANAGEMENT - إدارة الحلول
    # ═══════════════════════════════════════════════════════════
    
    def save_solution(
        self,
        problem: str,
        solution: str,
        rating: int = 5,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> int:
        """
        Save a solution to memory.
        حفظ حل في الذاكرة.
        
        Args:
            problem: Problem description
            solution: Solution text
            rating: User rating (1-5 stars)
            category: Optional category
            tags: Optional tags list
        
        Returns:
            Solution ID
        """
        cursor = self.conn.cursor()
        
        tags_str = ",".join(tags) if tags else None
        
        cursor.execute("""
            INSERT INTO solutions (problem, solution, rating, timestamp, category, tags)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (problem, solution, rating, datetime.now().isoformat(), category, tags_str))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def search_similar(self, problem: str, limit: int = 3) -> List[Tuple[str, int]]:
        """
        Search for similar past solutions.
        البحث عن حلول سابقة مشابهة.
        
        Args:
            problem: Problem to search for
            limit: Maximum number of results
        
        Returns:
            List of (solution, rating) tuples
        """
        cursor = self.conn.cursor()
        
        # Simple keyword-based search (can be improved with semantic search)
        keywords = problem.lower().split()
        
        # Build LIKE query for each keyword
        like_conditions = " OR ".join(["problem LIKE ?" for _ in keywords])
        like_params = [f"%{keyword}%" for keyword in keywords]
        
        cursor.execute(f"""
            SELECT solution, rating, success_count
            FROM solutions
            WHERE {like_conditions}
            ORDER BY rating DESC, success_count DESC
            LIMIT ?
        """, like_params + [limit])
        
        results = cursor.fetchall()
        return [(solution, rating) for solution, rating, _ in results]
    
    def increment_success_count(self, solution_id: int):
        """
        Increment success count for a solution.
        زيادة عداد النجاح لحل معين.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE solutions
            SET success_count = success_count + 1
            WHERE id = ?
        """, (solution_id,))
        self.conn.commit()
    
    def get_all_solutions(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all solutions, optionally filtered by category.
        الحصول على جميع الحلول، مع إمكانية التصفية حسب الفئة.
        """
        cursor = self.conn.cursor()
        
        if category:
            cursor.execute("""
                SELECT id, problem, solution, rating, success_count, timestamp, category, tags
                FROM solutions
                WHERE category = ?
                ORDER BY rating DESC, success_count DESC
            """, (category,))
        else:
            cursor.execute("""
                SELECT id, problem, solution, rating, success_count, timestamp, category, tags
                FROM solutions
                ORDER BY rating DESC, success_count DESC
            """)
        
        results = []
        for row in cursor.fetchall():
            results.append({
                "id": row[0],
                "problem": row[1],
                "solution": row[2],
                "rating": row[3],
                "success_count": row[4],
                "timestamp": row[5],
                "category": row[6],
                "tags": row[7].split(",") if row[7] else []
            })
        
        return results
    
    # ═══════════════════════════════════════════════════════════
    # CUSTOM TOOLS MANAGEMENT - إدارة الأدوات المخصصة
    # ═══════════════════════════════════════════════════════════
    
    def add_custom_tool(self, name: str, command: str, description: str) -> int:
        """
        Add a custom tool to memory.
        إضافة أداة مخصصة للذاكرة.
        """
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO custom_tools (name, command, description, created_at)
                VALUES (?, ?, ?, ?)
            """, (name, command, description, datetime.now().isoformat()))
            
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Tool already exists, update it
            cursor.execute("""
                UPDATE custom_tools
                SET command = ?, description = ?
                WHERE name = ?
            """, (command, description, name))
            self.conn.commit()
            return 0
    
    def get_custom_tools(self) -> List[Dict[str, Any]]:
        """
        Get all custom tools.
        الحصول على جميع الأدوات المخصصة.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, name, command, description, usage_count, created_at
            FROM custom_tools
            ORDER BY usage_count DESC
        """)
        
        results = []
        for row in cursor.fetchall():
            results.append({
                "id": row[0],
                "name": row[1],
                "command": row[2],
                "description": row[3],
                "usage_count": row[4],
                "created_at": row[5]
            })
        
        return results
    
    def increment_tool_usage(self, tool_name: str):
        """
        Increment usage count for a custom tool.
        زيادة عداد الاستخدام لأداة مخصصة.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE custom_tools
            SET usage_count = usage_count + 1
            WHERE name = ?
        """, (tool_name,))
        self.conn.commit()
    
    # ═══════════════════════════════════════════════════════════
    # PACKAGE REGISTRY - سجل الحزم
    # ═══════════════════════════════════════════════════════════
    
    def register_package(self, package_name: str, package_manager: str, reason: str):
        """
        Register an installed package.
        تسجيل حزمة مثبتة.
        """
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO packages (package_name, package_manager, reason, installed_at)
                VALUES (?, ?, ?, ?)
            """, (package_name, package_manager, reason, datetime.now().isoformat()))
            self.conn.commit()
        except sqlite3.IntegrityError:
            # Package already registered
            pass
    
    def is_package_installed(self, package_name: str) -> bool:
        """
        Check if a package is registered as installed.
        فحص إذا كانت الحزمة مسجلة كمثبتة.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM packages WHERE package_name = ?
        """, (package_name,))
        
        return cursor.fetchone()[0] > 0
    
    def get_installed_packages(self) -> List[Dict[str, Any]]:
        """
        Get all installed packages.
        الحصول على جميع الحزم المثبتة.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT package_name, package_manager, reason, installed_at
            FROM packages
            ORDER BY installed_at DESC
        """)
        
        results = []
        for row in cursor.fetchall():
            results.append({
                "package_name": row[0],
                "package_manager": row[1],
                "reason": row[2],
                "installed_at": row[3]
            })
        
        return results
    
    # ═══════════════════════════════════════════════════════════
    # USER PREFERENCES - تفضيلات المستخدم
    # ═══════════════════════════════════════════════════════════
    
    def set_preference(self, key: str, value: str):
        """
        Set a user preference.
        تعيين تفضيل مستخدم.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO preferences (key, value, updated_at)
            VALUES (?, ?, ?)
        """, (key, value, datetime.now().isoformat()))
        self.conn.commit()
    
    def get_preference(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get a user preference.
        الحصول على تفضيل مستخدم.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT value FROM preferences WHERE key = ?
        """, (key,))
        
        result = cursor.fetchone()
        return result[0] if result else default
    
    # ═══════════════════════════════════════════════════════════
    # ERROR TRACKING - تتبع الأخطاء
    # ═══════════════════════════════════════════════════════════
    
    def log_error(self, error_message: str, solution: Optional[str] = None):
        """
        Log an error and its solution.
        تسجيل خطأ وحله.
        """
        cursor = self.conn.cursor()
        
        # Check if error already exists
        cursor.execute("""
            SELECT id FROM errors WHERE error_message = ?
        """, (error_message,))
        
        existing = cursor.fetchone()
        
        if existing:
            # Increment occurrence count
            cursor.execute("""
                UPDATE errors
                SET occurrence_count = occurrence_count + 1,
                    last_seen = ?,
                    solution = COALESCE(?, solution)
                WHERE id = ?
            """, (datetime.now().isoformat(), solution, existing[0]))
        else:
            # Insert new error
            cursor.execute("""
                INSERT INTO errors (error_message, solution, first_seen, last_seen)
                VALUES (?, ?, ?, ?)
            """, (error_message, solution, datetime.now().isoformat(), datetime.now().isoformat()))
        
        self.conn.commit()
    
    def get_error_solution(self, error_message: str) -> Optional[str]:
        """
        Get solution for a known error.
        الحصول على حل لخطأ معروف.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT solution FROM errors
            WHERE error_message LIKE ?
            AND solution IS NOT NULL
            ORDER BY occurrence_count DESC
            LIMIT 1
        """, (f"%{error_message}%",))
        
        result = cursor.fetchone()
        return result[0] if result else None
    
    # ═══════════════════════════════════════════════════════════
    # STATISTICS - الإحصائيات
    # ═══════════════════════════════════════════════════════════
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get memory statistics.
        الحصول على إحصائيات الذاكرة.
        """
        cursor = self.conn.cursor()
        
        stats = {}
        
        # Solutions count
        cursor.execute("SELECT COUNT(*) FROM solutions")
        stats['total_solutions'] = cursor.fetchone()[0]
        
        # Custom tools count
        cursor.execute("SELECT COUNT(*) FROM custom_tools")
        stats['total_custom_tools'] = cursor.fetchone()[0]
        
        # Packages count
        cursor.execute("SELECT COUNT(*) FROM packages")
        stats['total_packages'] = cursor.fetchone()[0]
        
        # Average solution rating
        cursor.execute("SELECT AVG(rating) FROM solutions")
        avg_rating = cursor.fetchone()[0]
        stats['average_rating'] = round(avg_rating, 2) if avg_rating else 0
        
        # Most successful solution
        cursor.execute("""
            SELECT problem, success_count
            FROM solutions
            ORDER BY success_count DESC
            LIMIT 1
        """)
        top_solution = cursor.fetchone()
        if top_solution:
            stats['most_successful_solution'] = {
                "problem": top_solution[0],
                "success_count": top_solution[1]
            }
        
        return stats
    
    def close(self):
        """Close database connection."""
        self.conn.close()
    
    def __del__(self):
        """Cleanup on deletion."""
        try:
            self.conn.close()
        except:
            pass
