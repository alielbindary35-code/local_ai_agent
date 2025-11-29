"""
Memory System - Persistent learning and knowledge storage

SQLite-based memory system that stores solutions, custom tools,
package registry, and user preferences.

Now integrated with KnowledgeBase for enhanced learning.
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Tuple, Dict, Any, Optional
from pathlib import Path

# Import paths system
from src.core.paths import get_memory_db_file


class Memory:
    """
    Advanced learning and memory system for the AI agent.
    """
    
    def __init__(self, db_path: Optional[str] = None, knowledge_base=None):
        """
        Initialize memory system.
        
        Args:
            db_path: Path to SQLite database file (defaults to centralized path)
            knowledge_base: Optional KnowledgeBase instance for integration
        """
        if db_path is None:
            db_path = get_memory_db_file()
        self.db_path = str(db_path)
        # Use check_same_thread=False to allow use in different threads
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.knowledge_base = knowledge_base  # Optional integration
        self.create_tables()
    
    def create_tables(self):
        """
        Create database tables if they don't exist.
        """
        cursor = self.conn.cursor()
        
        # Solutions table
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
        
        # Create indexes for better search performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_solutions_problem ON solutions(problem)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_solutions_category ON solutions(category)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_solutions_rating ON solutions(rating DESC)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_solutions_timestamp ON solutions(timestamp DESC)
        """)
        
        # Custom tools table
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
        
        # Package registry
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                package_name TEXT UNIQUE NOT NULL,
                package_manager TEXT NOT NULL,
                reason TEXT,
                installed_at TEXT NOT NULL
            )
        """)
        
        # User preferences - 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS preferences (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        # Error patterns - 
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
        
        # Conversation history table for multi-turn conversations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                turn_number INTEGER NOT NULL,
                user_input TEXT NOT NULL,
                agent_response TEXT NOT NULL,
                context_data TEXT,
                tools_used TEXT,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """)
        
        # Sessions table for tracking conversation sessions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                started_at TEXT NOT NULL,
                last_activity TEXT NOT NULL,
                turn_count INTEGER DEFAULT 0,
                summary TEXT
            )
        """)
        
        # Create indexes for conversation history
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_conv_session ON conversation_history(session_id, turn_number)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_conv_timestamp ON conversation_history(timestamp DESC)
        """)
        
        self.conn.commit()
    
    # ═══════════════════════════════════════════════════════════
    # SOLUTIONS MANAGEMENT - 
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
        
        solution_id = cursor.lastrowid
        self.conn.commit()
        
        # Also store in KnowledgeBase if available
        if self.knowledge_base:
            try:
                confidence = rating / 5.0  # Convert rating to confidence
                self.knowledge_base.store_knowledge(
                    topic=problem,
                    content=solution,
                    category=category,
                    tags=tags,
                    source="memory_solution",
                    confidence=confidence
                )
            except Exception as e:
                # Don't fail if KnowledgeBase storage fails
                pass
        
        return solution_id
    
    def search_similar(self, problem: str, limit: int = 3) -> List[Tuple[str, int]]:
        """
        Search for similar past solutions with improved search algorithm.
        
        
        Args:
            problem: Problem to search for
            limit: Maximum number of results
        
        Returns:
            List of (solution, rating) tuples
        """
        cursor = self.conn.cursor()
        
        # Improved search: use FTS (Full-Text Search) if available, otherwise use LIKE
        # Remove common stop words for better matching
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        keywords = [word.lower() for word in problem.split() if word.lower() not in stop_words and len(word) > 2]
        
        if not keywords:
            keywords = problem.lower().split()
        
        # Build improved LIKE query with AND logic for better relevance
        like_conditions = " AND ".join(["problem LIKE ?" for _ in keywords])
        like_params = [f"%{keyword}%" for keyword in keywords]
        
        # Use scoring: prioritize solutions with more keyword matches
        cursor.execute(f"""
            SELECT solution, rating, success_count,
                   (rating * 0.4 + success_count * 0.3 + 
                    CASE WHEN problem LIKE ? THEN 10 ELSE 0 END) as score
            FROM solutions
            WHERE {like_conditions}
            ORDER BY score DESC, rating DESC, success_count DESC
            LIMIT ?
        """, like_params + [f"%{problem.lower()}%"] + [limit])
        
        results = cursor.fetchall()
        return [(solution, rating) for solution, rating, _, _ in results]
    
    def increment_success_count(self, solution_id: int):
        """
        Increment success count for a solution.
        
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
    # CUSTOM TOOLS MANAGEMENT - 
    # ═══════════════════════════════════════════════════════════
    
    def add_custom_tool(self, name: str, command: str, description: str) -> int:
        """
        Add a custom tool to memory.
        
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
        
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE custom_tools
            SET usage_count = usage_count + 1
            WHERE name = ?
        """, (tool_name,))
        self.conn.commit()
    
    # ═══════════════════════════════════════════════════════════
    # PACKAGE REGISTRY - 
    # ═══════════════════════════════════════════════════════════
    
    def register_package(self, package_name: str, package_manager: str, reason: str):
        """
        Register an installed package.
        
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
        
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM packages WHERE package_name = ?
        """, (package_name,))
        
        return cursor.fetchone()[0] > 0
    
    def get_installed_packages(self) -> List[Dict[str, Any]]:
        """
        Get all installed packages.
        
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
    # USER PREFERENCES - 
    # ═══════════════════════════════════════════════════════════
    
    def set_preference(self, key: str, value: str):
        """
        Set a user preference.
        
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
        
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT value FROM preferences WHERE key = ?
        """, (key,))
        
        result = cursor.fetchone()
        return result[0] if result else default
    
    # ═══════════════════════════════════════════════════════════
    # ERROR TRACKING - 
    # ═══════════════════════════════════════════════════════════
    
    def log_error(self, error_message: str, solution: Optional[str] = None):
        """
        Log an error and its solution.
        
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
    # STATISTICS - 
    # ═══════════════════════════════════════════════════════════
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get memory statistics.
        
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
    
    # ═══════════════════════════════════════════════════════════
    # CONVERSATION HISTORY MANAGEMENT
    # ═══════════════════════════════════════════════════════════
    
    def create_session(self, session_id: Optional[str] = None) -> str:
        """
        Create a new conversation session.
        
        Args:
            session_id: Optional session ID (generated if not provided)
        
        Returns:
            Session ID
        """
        import uuid
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        cursor = self.conn.cursor()
        now = datetime.now().isoformat()
        
        cursor.execute("""
            INSERT OR IGNORE INTO sessions (session_id, started_at, last_activity, turn_count)
            VALUES (?, ?, ?, 0)
        """, (session_id, now, now))
        
        self.conn.commit()
        return session_id
    
    def save_conversation_turn(
        self,
        session_id: str,
        user_input: str,
        agent_response: str,
        context_data: Optional[Dict[str, Any]] = None,
        tools_used: Optional[List[str]] = None
    ) -> int:
        """
        Save a conversation turn to history.
        
        Args:
            session_id: Session ID
            user_input: User's input
            agent_response: Agent's response
            context_data: Optional context data (JSON)
            tools_used: Optional list of tools used
        
        Returns:
            Turn ID
        """
        cursor = self.conn.cursor()
        
        # Get current turn number
        cursor.execute("""
            SELECT COALESCE(MAX(turn_number), 0) + 1
            FROM conversation_history
            WHERE session_id = ?
        """, (session_id,))
        turn_number = cursor.fetchone()[0]
        
        # Update session
        now = datetime.now().isoformat()
        cursor.execute("""
            UPDATE sessions
            SET last_activity = ?, turn_count = ?
            WHERE session_id = ?
        """, (now, turn_number, session_id))
        
        # Save conversation turn
        context_json = json.dumps(context_data) if context_data else None
        tools_json = json.dumps(tools_used) if tools_used else None
        
        cursor.execute("""
            INSERT INTO conversation_history 
            (session_id, turn_number, user_input, agent_response, context_data, tools_used, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (session_id, turn_number, user_input, agent_response, context_json, tools_json, now))
        
        turn_id = cursor.lastrowid
        self.conn.commit()
        return turn_id
    
    def get_conversation_history(
        self,
        session_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get conversation history for a session.
        
        Args:
            session_id: Session ID
            limit: Maximum number of turns to retrieve
        
        Returns:
            List of conversation turns
        """
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT turn_number, user_input, agent_response, context_data, tools_used, timestamp
            FROM conversation_history
            WHERE session_id = ?
            ORDER BY turn_number DESC
            LIMIT ?
        """, (session_id, limit))
        
        turns = []
        for row in cursor.fetchall():
            turn_num, user_input, agent_response, context_data, tools_used, timestamp = row
            turn = {
                "turn_number": turn_num,
                "user_input": user_input,
                "agent_response": agent_response,
                "context_data": json.loads(context_data) if context_data else None,
                "tools_used": json.loads(tools_used) if tools_used else None,
                "timestamp": timestamp
            }
            turns.append(turn)
        
        # Return in chronological order
        return list(reversed(turns))
    
    def get_recent_context(
        self,
        session_id: str,
        turns: int = 3
    ) -> str:
        """
        Get recent conversation context as formatted string.
        
        Args:
            session_id: Session ID
            turns: Number of recent turns to include
        
        Returns:
            Formatted context string
        """
        history = self.get_conversation_history(session_id, limit=turns)
        
        if not history:
            return ""
        
        context_parts = []
        for turn in history:
            context_parts.append(f"User: {turn['user_input']}")
            context_parts.append(f"Agent: {turn['agent_response'][:200]}...")  # Truncate long responses
        
        return "\n".join(context_parts)
    
    def summarize_session(self, session_id: str) -> Optional[str]:
        """
        Generate a summary of a conversation session.
        
        Args:
            session_id: Session ID
        
        Returns:
            Session summary or None
        """
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT turn_count, started_at, last_activity
            FROM sessions
            WHERE session_id = ?
        """, (session_id,))
        
        session_data = cursor.fetchone()
        if not session_data:
            return None
        
        turn_count, started_at, last_activity = session_data
        
        history = self.get_conversation_history(session_id, limit=5)
        
        summary = f"Session: {session_id}\n"
        summary += f"Turns: {turn_count}\n"
        summary += f"Started: {started_at}\n"
        summary += f"Last Activity: {last_activity}\n"
        summary += f"Recent Topics: {', '.join([turn['user_input'][:50] for turn in history[:3]])}"
        
        return summary
    
    def close(self):
        """Close database connection."""
        self.conn.close()
    
    def __del__(self):
        """Cleanup on deletion."""
        try:
            self.conn.close()
        except:
            pass
