"""
Knowledge Base System - Advanced Learning and Knowledge Storage
===============================================================

A comprehensive knowledge management system that:
- Stores knowledge locally in structured format
- Retrieves knowledge with pattern matching
- Automatically learns from interactions
- Integrates with AI models for knowledge enhancement
- Works completely offline
"""

import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import re
from difflib import SequenceMatcher

# Import paths system
from src.core.paths import get_knowledge_base_dir, get_memory_db_file, ensure_dir


class KnowledgeBase:
    """
    Advanced Knowledge Base System for AI Agent
    
    Features:
    - Structured knowledge storage (SQLite + file-based)
    - Pattern matching and similarity search
    - Automatic learning evaluation
    - Knowledge enhancement with AI models
    - Offline-first with caching
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize Knowledge Base system
        
        Args:
            db_path: Path to SQLite database (defaults to memory DB)
        """
        if db_path is None:
            db_path = get_memory_db_file()
        
        self.db_path = str(db_path)
        self.kb_dir = get_knowledge_base_dir()
        ensure_dir(self.kb_dir)
        
        # Initialize database connection
        # Use check_same_thread=False to allow use in different threads
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.create_tables()
        
        # In-memory cache for frequently accessed knowledge
        self._cache: Dict[str, Any] = {}
        self._cache_max_size = 100  # Maximum cached items
        
    def create_tables(self):
        """Create knowledge base tables if they don't exist"""
        cursor = self.conn.cursor()
        
        # Knowledge entries table - stores structured knowledge
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                content TEXT NOT NULL,
                category TEXT,
                tags TEXT,
                source TEXT,
                confidence REAL DEFAULT 1.0,
                usage_count INTEGER DEFAULT 0,
                last_used TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        # Knowledge patterns table - stores patterns for matching
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern TEXT NOT NULL,
                topic_id INTEGER,
                pattern_type TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (topic_id) REFERENCES knowledge_entries(id)
            )
        """)
        
        # Learning history table - tracks what was learned
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                interaction_id TEXT,
                user_input TEXT,
                learned_content TEXT,
                knowledge_type TEXT,
                was_useful BOOLEAN,
                created_at TEXT NOT NULL
            )
        """)
        
        # Create indexes for better performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_knowledge_topic ON knowledge_entries(topic)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_knowledge_category ON knowledge_entries(category)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_knowledge_tags ON knowledge_entries(tags)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_patterns_pattern ON knowledge_patterns(pattern)
        """)
        
        self.conn.commit()
    
    # ═══════════════════════════════════════════════════════════
    # KNOWLEDGE STORAGE
    # ═══════════════════════════════════════════════════════════
    
    def store_knowledge(
        self,
        topic: str,
        content: str,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        source: Optional[str] = None,
        confidence: float = 1.0
    ) -> int:
        """
        Store knowledge in the database
        
        Args:
            topic: Main topic/subject
            content: Knowledge content
            category: Category (e.g., "programming", "docker", "database")
            tags: List of tags
            source: Source of knowledge (e.g., "user_interaction", "web_search", "ai_generated")
            confidence: Confidence level (0.0 to 1.0)
        
        Returns:
            Knowledge entry ID
        """
        cursor = self.conn.cursor()
        
        tags_str = ",".join(tags) if tags else None
        now = datetime.now().isoformat()
        
        cursor.execute("""
            INSERT INTO knowledge_entries 
            (topic, content, category, tags, source, confidence, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (topic, content, category, tags_str, source, confidence, now, now))
        
        entry_id = cursor.lastrowid
        
        # Extract and store patterns
        self._extract_and_store_patterns(entry_id, topic, content)
        
        # Update cache
        cache_key = f"{topic}:{category}"
        if cache_key in self._cache:
            del self._cache[cache_key]
        
        self.conn.commit()
        return entry_id
    
    def _extract_and_store_patterns(self, entry_id: int, topic: str, content: str):
        """Extract patterns from knowledge for better matching"""
        cursor = self.conn.cursor()
        
        patterns = []
        
        # Extract keywords from topic
        keywords = re.findall(r'\b\w{3,}\b', topic.lower())
        patterns.extend([(kw, "keyword") for kw in keywords[:10]])  # Limit to 10 keywords
        
        # Extract key phrases from content (first 500 chars)
        content_preview = content[:500].lower()
        phrases = re.findall(r'\b\w{4,}\b', content_preview)
        # Get most common phrases
        from collections import Counter
        common_phrases = [p for p, _ in Counter(phrases).most_common(5)]
        patterns.extend([(p, "content_phrase") for p in common_phrases])
        
        # Store patterns
        now = datetime.now().isoformat()
        for pattern, pattern_type in patterns:
            cursor.execute("""
                INSERT INTO knowledge_patterns (pattern, topic_id, pattern_type, created_at)
                VALUES (?, ?, ?, ?)
            """, (pattern, entry_id, pattern_type, now))
    
    # ═══════════════════════════════════════════════════════════
    # KNOWLEDGE RETRIEVAL
    # ═══════════════════════════════════════════════════════════
    
    def retrieve_knowledge(
        self,
        query: str,
        category: Optional[str] = None,
        limit: int = 5,
        min_confidence: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve knowledge matching the query
        
        Args:
            query: Search query
            category: Optional category filter
            limit: Maximum number of results
            min_confidence: Minimum confidence threshold
        
        Returns:
            List of knowledge entries with relevance scores
        """
        # Check cache first
        cache_key = f"query:{query}:{category}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        cursor = self.conn.cursor()
        query_lower = query.lower()
        
        # Extract keywords from query
        keywords = re.findall(r'\b\w{3,}\b', query_lower)
        
        # Build search query with pattern matching
        results = []
        
        # Method 1: Direct topic/content match
        if category:
            cursor.execute("""
                SELECT id, topic, content, category, tags, confidence, usage_count
                FROM knowledge_entries
                WHERE category = ? AND confidence >= ?
                ORDER BY usage_count DESC, confidence DESC
                LIMIT ?
            """, (category, min_confidence, limit))
        else:
            cursor.execute("""
                SELECT id, topic, content, category, tags, confidence, usage_count
                FROM knowledge_entries
                WHERE confidence >= ?
                ORDER BY usage_count DESC, confidence DESC
                LIMIT ?
            """, (min_confidence, limit))
        
        for row in cursor.fetchall():
            entry_id, topic, content, cat, tags, conf, usage = row
            score = self._calculate_relevance_score(query, topic, content, keywords)
            if score > 0.3:  # Minimum relevance threshold
                results.append({
                    "id": entry_id,
                    "topic": topic,
                    "content": content,
                    "category": cat,
                    "tags": tags.split(",") if tags else [],
                    "confidence": conf,
                    "usage_count": usage,
                    "relevance_score": score
                })
        
        # Method 2: Pattern matching
        if len(results) < limit:
            pattern_results = self._search_by_patterns(keywords, category, limit - len(results))
            results.extend(pattern_results)
        
        # Sort by relevance score
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        results = results[:limit]
        
        # Update usage counts
        for result in results:
            self._increment_usage(result["id"])
        
        # Cache results
        if len(self._cache) >= self._cache_max_size:
            # Remove oldest cache entry (simple FIFO)
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        self._cache[cache_key] = results
        
        return results
    
    def _calculate_relevance_score(
        self,
        query: str,
        topic: str,
        content: str,
        keywords: List[str]
    ) -> float:
        """Calculate relevance score between query and knowledge entry"""
        score = 0.0
        
        query_lower = query.lower()
        topic_lower = topic.lower()
        content_lower = content[:500].lower()  # Use first 500 chars for performance
        
        # Exact topic match
        if query_lower in topic_lower or topic_lower in query_lower:
            score += 0.5
        
        # Keyword matching in topic
        topic_matches = sum(1 for kw in keywords if kw in topic_lower)
        if keywords:
            score += (topic_matches / len(keywords)) * 0.3
        
        # Keyword matching in content
        content_matches = sum(1 for kw in keywords if kw in content_lower)
        if keywords:
            score += (content_matches / len(keywords)) * 0.2
        
        # String similarity
        topic_similarity = SequenceMatcher(None, query_lower, topic_lower).ratio()
        score += topic_similarity * 0.2
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _search_by_patterns(
        self,
        keywords: List[str],
        category: Optional[str],
        limit: int
    ) -> List[Dict[str, Any]]:
        """Search knowledge using stored patterns"""
        if not keywords:
            return []
        
        cursor = self.conn.cursor()
        results = []
        
        # Find patterns matching keywords
        placeholders = ",".join(["?"] * len(keywords))
        query = f"""
            SELECT DISTINCT ke.id, ke.topic, ke.content, ke.category, ke.tags, ke.confidence, ke.usage_count
            FROM knowledge_entries ke
            JOIN knowledge_patterns kp ON ke.id = kp.topic_id
            WHERE kp.pattern IN ({placeholders})
        """
        params = list(keywords)
        
        if category:
            query += " AND ke.category = ?"
            params.append(category)
        
        query += " ORDER BY ke.usage_count DESC, ke.confidence DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        
        for row in cursor.fetchall():
            entry_id, topic, content, cat, tags, conf, usage = row
            results.append({
                "id": entry_id,
                "topic": topic,
                "content": content,
                "category": cat,
                "tags": tags.split(",") if tags else [] if tags else [],
                "confidence": conf,
                "usage_count": usage,
                "relevance_score": 0.4  # Default score for pattern matches
            })
        
        return results
    
    def _increment_usage(self, entry_id: int):
        """Increment usage count for a knowledge entry"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE knowledge_entries
            SET usage_count = usage_count + 1,
                last_used = ?
            WHERE id = ?
        """, (datetime.now().isoformat(), entry_id))
        self.conn.commit()
    
    # ═══════════════════════════════════════════════════════════
    # AUTOMATIC LEARNING EVALUATION
    # ═══════════════════════════════════════════════════════════
    
    def should_learn(
        self,
        user_input: str,
        agent_response: str,
        interaction_context: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, str, float]:
        """
        Determine if the agent should learn from this interaction
        
        Args:
            user_input: User's input/question
            agent_response: Agent's response
            interaction_context: Additional context (tools used, etc.)
        
        Returns:
            Tuple of (should_learn, knowledge_type, confidence)
        """
        # Don't learn from errors
        if "Error:" in agent_response or "error" in agent_response.lower():
            return (False, "error", 0.0)
        
        # Check if this is a question-answer pair
        is_question = any(marker in user_input for marker in ["?", "what", "how", "why", "when", "where", "explain", "tell me"])
        
        # Check if response contains substantial information
        response_length = len(agent_response)
        has_substantial_content = response_length > 100
        
        # Check if tools were used (indicates actionable knowledge)
        tools_used = []
        if interaction_context:
            tools_used = interaction_context.get("tools_used", [])
        
        # Determine knowledge type
        knowledge_type = "general"
        confidence = 0.5
        
        if is_question and has_substantial_content:
            # Q&A knowledge
            knowledge_type = "qa"
            confidence = 0.7
            
            # Check if it's technology-specific
            tech_keywords = ["docker", "python", "javascript", "postgres", "n8n", "react", "vue", "flask", "django"]
            for tech in tech_keywords:
                if tech in user_input.lower() or tech in agent_response.lower():
                    knowledge_type = f"tech_{tech}"
                    confidence = 0.8
                    break
        
        if tools_used:
            # Tool usage knowledge
            if "learn" in str(tools_used).lower() or "search" in str(tools_used).lower():
                knowledge_type = "learning"
                confidence = 0.9
        
        # Check if response contains code
        if "```" in agent_response or "def " in agent_response or "function " in agent_response:
            knowledge_type = "code_solution"
            confidence = 0.85
        
        # Final decision
        should_learn = (
            has_substantial_content and
            confidence >= 0.5 and
            response_length > 50
        )
        
        return (should_learn, knowledge_type, confidence)
    
    def learn_from_interaction(
        self,
        user_input: str,
        agent_response: str,
        interaction_context: Optional[Dict[str, Any]] = None
    ) -> Optional[int]:
        """
        Learn from an interaction and store knowledge
        
        Returns:
            Knowledge entry ID if stored, None otherwise
        """
        should_learn, knowledge_type, confidence = self.should_learn(
            user_input, agent_response, interaction_context
        )
        
        if not should_learn:
            return None
        
        # Extract category from context or user input
        category = None
        if interaction_context:
            category = interaction_context.get("category")
        
        if not category:
            # Try to detect category from input
            category = self._detect_category(user_input)
        
        # Extract tags
        tags = self._extract_tags(user_input, agent_response)
        
        # Store knowledge
        entry_id = self.store_knowledge(
            topic=user_input[:200],  # Truncate if too long
            content=agent_response,
            category=category,
            tags=tags,
            source="user_interaction",
            confidence=confidence
        )
        
        # Log learning history
        self._log_learning(user_input, agent_response, knowledge_type)
        
        return entry_id
    
    def _detect_category(self, user_input: str) -> Optional[str]:
        """Detect category from user input"""
        categories = {
            "programming": ["code", "function", "class", "python", "javascript", "java", "programming"],
            "docker": ["docker", "container", "dockerfile", "compose"],
            "database": ["database", "sql", "postgres", "mysql", "query"],
            "web": ["html", "css", "website", "frontend", "backend", "react", "vue"],
            "devops": ["deploy", "server", "nginx", "ssl", "ci/cd"],
            "automation": ["n8n", "workflow", "automation"],
        }
        
        user_lower = user_input.lower()
        for cat, keywords in categories.items():
            if any(kw in user_lower for kw in keywords):
                return cat
        
        return "general"
    
    def _extract_tags(self, user_input: str, response: str) -> List[str]:
        """Extract relevant tags from input and response"""
        tags = []
        
        # Extract technology names
        tech_keywords = [
            "docker", "python", "javascript", "postgres", "n8n", "react", "vue",
            "flask", "django", "fastapi", "node", "express", "html", "css"
        ]
        
        combined = (user_input + " " + response).lower()
        for tech in tech_keywords:
            if tech in combined:
                tags.append(tech)
        
        return tags[:5]  # Limit to 5 tags
    
    def _log_learning(self, user_input: str, response: str, knowledge_type: str):
        """Log learning activity"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO learning_history 
            (user_input, learned_content, knowledge_type, was_useful, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            user_input[:500],
            response[:1000],
            knowledge_type,
            True,  # Assume useful if we're storing it
            datetime.now().isoformat()
        ))
        self.conn.commit()
    
    # ═══════════════════════════════════════════════════════════
    # KNOWLEDGE ENHANCEMENT WITH AI
    # ═══════════════════════════════════════════════════════════
    
    def enhance_knowledge_with_ai(
        self,
        knowledge_id: int,
        ollama_url: str = "http://localhost:11434",
        model: str = "qwen2.5:3b"
    ) -> bool:
        """
        Enhance knowledge entry using AI model
        
        Args:
            knowledge_id: ID of knowledge entry to enhance
            ollama_url: Ollama API URL
            model: Model to use for enhancement
        
        Returns:
            True if enhancement successful
        """
        try:
            # Create a new database connection for this thread
            # SQLite connections cannot be shared across threads
            import sqlite3
            thread_conn = sqlite3.connect(self.db_path)
            
            try:
                # Get knowledge entry
                cursor = thread_conn.cursor()
                cursor.execute("""
                    SELECT topic, content, category FROM knowledge_entries WHERE id = ?
                """, (knowledge_id,))
                
                row = cursor.fetchone()
                if not row:
                    thread_conn.close()
                    return False
                
                topic, content, category = row
                
                # Use AI to enhance/summarize
                import requests
                
                prompt = f"""Please enhance and summarize the following knowledge:

Topic: {topic}
Category: {category or 'general'}

Content:
{content[:2000]}

Provide:
1. A concise summary (2-3 sentences)
2. Key points (bullet list)
3. Related concepts

Format as markdown."""

                response = requests.post(
                    f"{ollama_url}/api/generate",
                    json={
                        "model": model,
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=60
                )
                
                if response.status_code == 200:
                    enhanced_content = response.json().get("response", "")
                    
                    # Update knowledge entry
                    cursor.execute("""
                        UPDATE knowledge_entries
                        SET content = ?,
                            updated_at = ?,
                            confidence = confidence + 0.1
                        WHERE id = ?
                    """, (
                        f"{content}\n\n--- AI Enhanced ---\n\n{enhanced_content}",
                        datetime.now().isoformat(),
                        knowledge_id
                    ))
                    
                    thread_conn.commit()
                    thread_conn.close()
                    return True
                
                thread_conn.close()
                return False
            
            except Exception as e:
                thread_conn.close()
                raise e
        
        except Exception as e:
            print(f"Error enhancing knowledge: {e}")
            return False
    
    # ═══════════════════════════════════════════════════════════
    # STATISTICS AND MANAGEMENT
    # ═══════════════════════════════════════════════════════════
    
    def delete_entry(self, entry_id: int) -> bool:
        """
        Delete a knowledge entry
        
        Args:
            entry_id: ID of entry to delete
        
        Returns:
            True if deleted successfully
        """
        try:
            cursor = self.conn.cursor()
            
            # Delete associated patterns first
            cursor.execute("DELETE FROM knowledge_patterns WHERE topic_id = ?", (entry_id,))
            
            # Delete the entry
            cursor.execute("DELETE FROM knowledge_entries WHERE id = ?", (entry_id,))
            
            self.conn.commit()
            
            # Clear cache
            self.clear_cache()
            
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting entry: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge base statistics"""
        cursor = self.conn.cursor()
        
        stats = {}
        
        # Total entries
        cursor.execute("SELECT COUNT(*) FROM knowledge_entries")
        stats["total_entries"] = cursor.fetchone()[0]
        
        # By category
        cursor.execute("""
            SELECT category, COUNT(*) 
            FROM knowledge_entries 
            GROUP BY category
        """)
        stats["by_category"] = dict(cursor.fetchall())
        
        # Most used
        cursor.execute("""
            SELECT topic, usage_count 
            FROM knowledge_entries 
            ORDER BY usage_count DESC 
            LIMIT 5
        """)
        stats["most_used"] = cursor.fetchall()
        
        # Learning history count
        cursor.execute("SELECT COUNT(*) FROM learning_history")
        stats["total_learned"] = cursor.fetchone()[0]
        
        return stats
    
    def clear_cache(self):
        """Clear the knowledge cache"""
        self._cache.clear()
    
    def close(self):
        """Close database connection"""
        self.conn.close()
    
    def __del__(self):
        """Cleanup on deletion"""
        try:
            self.conn.close()
        except:
            pass

