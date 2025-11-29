"""
Comprehensive tests for KnowledgeBase system
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from src.core.knowledge_base import KnowledgeBase


@pytest.fixture
def temp_db():
    """Create temporary database for tests"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    yield db_path
    # Cleanup
    if Path(db_path).exists():
        Path(db_path).unlink()


@pytest.fixture
def temp_kb_dir():
    """Create temporary knowledge base directory"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def knowledge_base(temp_db, temp_kb_dir):
    """Create KnowledgeBase instance"""
    with patch('src.core.knowledge_base.get_knowledge_base_dir', return_value=temp_kb_dir):
        with patch('src.core.knowledge_base.ensure_dir'):
            kb = KnowledgeBase(db_path=temp_db)
            yield kb


class TestKnowledgeBase:
    """Tests for KnowledgeBase class"""
    
    def test_knowledge_base_initialization(self, knowledge_base):
        """Test knowledge base initializes correctly"""
        assert knowledge_base.db_path is not None
        assert knowledge_base.conn is not None
        assert knowledge_base.kb_dir is not None
    
    def test_create_tables(self, knowledge_base):
        """Test tables are created"""
        cursor = knowledge_base.conn.cursor()
        
        # Check knowledge_entries table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='knowledge_entries'")
        assert cursor.fetchone() is not None
        
        # Check knowledge_patterns table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='knowledge_patterns'")
        assert cursor.fetchone() is not None
    
    def test_store_knowledge(self, knowledge_base):
        """Test storing knowledge"""
        kb_id = knowledge_base.store_knowledge(
            topic="Python Basics",
            content="Python is a programming language...",
            category="programming",
            tags=["python", "basics"],
            source="manual",
            confidence=0.9
        )
        
        assert kb_id is not None
        assert isinstance(kb_id, int)
        
        # Verify stored
        cursor = knowledge_base.conn.cursor()
        cursor.execute("SELECT * FROM knowledge_entries WHERE id=?", (kb_id,))
        result = cursor.fetchone()
        
        assert result is not None
        assert result[1] == "Python Basics"
        assert result[2] == "Python is a programming language..."
    
    def test_retrieve_knowledge(self, knowledge_base):
        """Test retrieving knowledge"""
        # Store some knowledge
        knowledge_base.store_knowledge(
            topic="Docker Commands",
            content="docker run, docker build, docker compose",
            category="docker",
            tags=["docker", "commands"]
        )
        
        # Retrieve
        results = knowledge_base.retrieve_knowledge(
            query="docker commands",
            category="docker",
            limit=5
        )
        
        assert len(results) > 0
        assert any("Docker" in result.get('topic', '') for result in results)
    
    def test_learn_from_interaction(self, knowledge_base):
        """Test learning from interaction"""
        interaction_id = knowledge_base.learn_from_interaction(
            user_input="how to use docker",
            agent_response="Use docker run command",
            interaction_context={"tools_used": ["docker_command"]}
        )
        
        assert interaction_id is not None
        
        # Check learning history
        cursor = knowledge_base.conn.cursor()
        cursor.execute("SELECT * FROM learning_history WHERE interaction_id=?", (interaction_id,))
        result = cursor.fetchone()
        
        assert result is not None
    
    def test_search_similar_topics(self, knowledge_base):
        """Test searching for similar topics"""
        # Store knowledge
        knowledge_base.store_knowledge(
            topic="Python Functions",
            content="def function_name(): pass",
            category="programming"
        )
        
        # Search
        results = knowledge_base.search_similar_topics("python function", limit=5)
        
        assert len(results) > 0
        assert any("function" in result.get('topic', '').lower() for result in results)
    
    def test_update_knowledge(self, knowledge_base):
        """Test updating knowledge"""
        # Store knowledge
        kb_id = knowledge_base.store_knowledge(
            topic="Test Topic",
            content="Original content",
            category="test"
        )
        
        # Update
        knowledge_base.update_knowledge(
            kb_id=kb_id,
            content="Updated content",
            confidence=0.95
        )
        
        # Verify update
        cursor = knowledge_base.conn.cursor()
        cursor.execute("SELECT content, confidence FROM knowledge_entries WHERE id=?", (kb_id,))
        result = cursor.fetchone()
        
        assert result[0] == "Updated content"
        assert result[1] == 0.95
    
    def test_delete_knowledge(self, knowledge_base):
        """Test deleting knowledge"""
        # Store knowledge
        kb_id = knowledge_base.store_knowledge(
            topic="To Delete",
            content="This will be deleted",
            category="test"
        )
        
        # Delete
        knowledge_base.delete_knowledge(kb_id)
        
        # Verify deleted
        cursor = knowledge_base.conn.cursor()
        cursor.execute("SELECT * FROM knowledge_entries WHERE id=?", (kb_id,))
        result = cursor.fetchone()
        
        assert result is None
    
    def test_get_statistics(self, knowledge_base):
        """Test getting knowledge base statistics"""
        # Add some knowledge
        knowledge_base.store_knowledge("Topic1", "Content1", category="cat1")
        knowledge_base.store_knowledge("Topic2", "Content2", category="cat2")
        
        stats = knowledge_base.get_statistics()
        
        assert isinstance(stats, dict)
        assert stats.get('total_entries', 0) >= 2

