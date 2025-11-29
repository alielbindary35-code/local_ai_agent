"""
Comprehensive tests for Memory system
"""

import pytest
import tempfile
import sqlite3
from pathlib import Path
from src.core.memory import Memory


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
def memory(temp_db):
    """Create Memory instance with temp database"""
    return Memory(db_path=temp_db)


class TestMemory:
    """Tests for Memory class"""
    
    def test_memory_initialization(self, memory):
        """Test memory initializes correctly"""
        assert memory.db_path is not None
        assert memory.conn is not None
    
    def test_create_tables(self, memory):
        """Test tables are created"""
        cursor = memory.conn.cursor()
        
        # Check solutions table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='solutions'")
        assert cursor.fetchone() is not None
        
        # Check custom_tools table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='custom_tools'")
        assert cursor.fetchone() is not None
        
        # Check packages table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='packages'")
        assert cursor.fetchone() is not None
    
    def test_save_solution(self, memory):
        """Test saving a solution"""
        memory.save_solution(
            problem="test problem",
            solution="test solution",
            rating=5
        )
        
        cursor = memory.conn.cursor()
        cursor.execute("SELECT * FROM solutions WHERE problem=?", ("test problem",))
        result = cursor.fetchone()
        
        assert result is not None
        assert result[1] == "test problem"
        assert result[2] == "test solution"
        assert result[3] == 5
    
    def test_search_similar(self, memory):
        """Test searching for similar solutions"""
        # Add some test solutions
        memory.save_solution("how to install python", "use pip install", rating=5)
        memory.save_solution("python installation", "install via pip", rating=4)
        memory.save_solution("docker setup", "use docker compose", rating=5)
        
        # Search for similar
        results = memory.search_similar("install python package")
        
        assert len(results) > 0
        # Should find python-related solutions
        assert any("python" in str(result[0]).lower() for result in results)
    
    def test_save_custom_tool(self, memory):
        """Test saving custom tool"""
        memory.save_custom_tool(
            name="test_tool",
            command="echo test",
            description="Test tool"
        )
        
        cursor = memory.conn.cursor()
        cursor.execute("SELECT * FROM custom_tools WHERE name=?", ("test_tool",))
        result = cursor.fetchone()
        
        assert result is not None
        assert result[1] == "test_tool"
        assert result[2] == "echo test"
    
    def test_get_custom_tools(self, memory):
        """Test getting custom tools"""
        # Add a custom tool
        memory.save_custom_tool("tool1", "cmd1", "desc1")
        memory.save_custom_tool("tool2", "cmd2", "desc2")
        
        tools = memory.get_custom_tools()
        
        assert len(tools) >= 2
        assert any(tool['name'] == 'tool1' for tool in tools)
        assert any(tool['name'] == 'tool2' for tool in tools)
    
    def test_save_package(self, memory):
        """Test saving package"""
        memory.save_package(
            package_name="requests",
            package_manager="pip",
            reason="HTTP library"
        )
        
        cursor = memory.conn.cursor()
        cursor.execute("SELECT * FROM packages WHERE package_name=?", ("requests",))
        result = cursor.fetchone()
        
        assert result is not None
        assert result[1] == "requests"
        assert result[2] == "pip"
    
    def test_get_statistics(self, memory):
        """Test getting memory statistics"""
        # Add some data
        memory.save_solution("problem1", "solution1", rating=5)
        memory.save_solution("problem2", "solution2", rating=4)
        memory.save_custom_tool("tool1", "cmd1", "desc1")
        memory.save_package("pkg1", "pip", "reason1")
        
        stats = memory.get_statistics()
        
        assert isinstance(stats, dict)
        assert stats.get('total_solutions', 0) >= 2
        assert stats.get('total_custom_tools', 0) >= 1
        assert stats.get('total_packages', 0) >= 1
    
    def test_update_solution_rating(self, memory):
        """Test updating solution rating"""
        memory.save_solution("test", "solution", rating=3)
        
        # Update rating
        memory.update_solution_rating("test", 5)
        
        cursor = memory.conn.cursor()
        cursor.execute("SELECT rating FROM solutions WHERE problem=?", ("test",))
        result = cursor.fetchone()
        
        assert result[0] == 5
    
    def test_increment_success_count(self, memory):
        """Test incrementing success count"""
        memory.save_solution("test", "solution", rating=5)
        
        # Increment success
        memory.increment_success_count("test")
        
        cursor = memory.conn.cursor()
        cursor.execute("SELECT success_count FROM solutions WHERE problem=?", ("test",))
        result = cursor.fetchone()
        
        assert result[0] >= 1

