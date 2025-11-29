"""
Comprehensive tests for Tools classes
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from src.tools.tools import Tools
from src.tools.expert_tools import ExpertTools
from src.tools.extended_tools import ExtendedTools


@pytest.fixture
def temp_dir():
    """Create temporary directory for tests"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def tools():
    """Create Tools instance"""
    return Tools()


class TestBasicTools:
    """Tests for basic Tools class"""
    
    def test_tools_initialization(self, tools):
        """Test tools initializes correctly"""
        assert tools.system is not None
        assert tools.custom_tools == {}
    
    def test_get_os_identifier(self, tools):
        """Test OS identification"""
        os_id = tools.get_os_identifier()
        assert isinstance(os_id, str)
        assert len(os_id) > 0
    
    def test_get_tool_descriptions(self, tools):
        """Test tool descriptions are returned"""
        descriptions = tools.get_tool_descriptions()
        assert isinstance(descriptions, str)
        assert 'read_file' in descriptions
        assert 'write_file' in descriptions
    
    def test_read_file(self, tools, temp_dir):
        """Test reading a file"""
        test_file = Path(temp_dir) / "test.txt"
        test_file.write_text("Hello, World!")
        
        result = tools.read_file(str(test_file))
        assert "Hello, World!" in result
    
    def test_write_file(self, tools, temp_dir):
        """Test writing a file"""
        test_file = Path(temp_dir) / "output.txt"
        content = "Test content"
        
        result = tools.write_file(str(test_file), content)
        assert "Successfully" in result or "written" in result.lower()
        assert test_file.exists()
        assert test_file.read_text() == content
    
    def test_create_directory(self, tools, temp_dir):
        """Test creating directory"""
        new_dir = Path(temp_dir) / "new_folder"
        
        result = tools.create_directory(str(new_dir))
        assert "Successfully" in result or "created" in result.lower()
        assert new_dir.exists()
        assert new_dir.is_dir()
    
    def test_list_dir(self, tools, temp_dir):
        """Test listing directory"""
        # Create some test files
        (Path(temp_dir) / "file1.txt").touch()
        (Path(temp_dir) / "file2.txt").touch()
        
        result = tools.list_dir(temp_dir)
        assert isinstance(result, str)
        assert "file1.txt" in result or "file2.txt" in result
    
    def test_search_files(self, tools, temp_dir):
        """Test searching for files"""
        # Create test files
        (Path(temp_dir) / "test1.txt").touch()
        (Path(temp_dir) / "test2.txt").touch()
        (Path(temp_dir) / "other.log").touch()
        
        result = tools.search_files("*.txt", temp_dir)
        assert isinstance(result, str)
        assert "test1.txt" in result or "test2.txt" in result
    
    @patch('subprocess.run')
    def test_run_command(self, mock_run, tools):
        """Test running a command"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "Command output"
        mock_run.return_value.stderr = ""
        
        result = tools.run_command("echo test")
        assert isinstance(result, str)
        mock_run.assert_called_once()
    
    def test_get_system_info(self, tools):
        """Test getting system information"""
        result = tools.get_system_info()
        assert isinstance(result, dict)
        assert 'os' in result or 'system' in result.lower()
    
    def test_monitor_resources(self, tools):
        """Test monitoring system resources"""
        result = tools.monitor_resources()
        assert isinstance(result, dict)
        assert 'cpu_percent' in result or 'memory_percent' in result
    
    @patch('src.tools.tools.DDGS')
    def test_search_web(self, mock_ddgs, tools):
        """Test web search"""
        mock_instance = MagicMock()
        mock_instance.text.return_value = [
            {'title': 'Test', 'body': 'Test body', 'href': 'http://test.com'}
        ]
        mock_ddgs.return_value = mock_instance
        
        result = tools.search_web("test query")
        assert isinstance(result, list)
        if result and len(result) > 0:
            assert isinstance(result[0], dict)
    
    def test_execute_invalid_tool(self, tools):
        """Test executing non-existent tool"""
        result = tools.execute("nonexistent_tool", {})
        assert "not found" in result.lower() or "Error" in result
    
    def test_register_custom_tool(self, tools):
        """Test registering custom tool"""
        result = tools.register_custom_tool(
            name="test_tool",
            command="echo test",
            description="Test tool"
        )
        assert "Successfully" in result or "registered" in result.lower()
        assert "test_tool" in tools.custom_tools


class TestExpertTools:
    """Tests for ExpertTools class"""
    
    @pytest.fixture
    def expert_tools(self):
        """Create ExpertTools instance"""
        return ExpertTools()
    
    def test_expert_tools_initialization(self, expert_tools):
        """Test expert tools initializes"""
        assert expert_tools is not None
    
    def test_get_tool_descriptions(self, expert_tools):
        """Test getting tool descriptions"""
        descriptions = expert_tools.get_tool_descriptions()
        assert isinstance(descriptions, str)
        assert len(descriptions) > 0
    
    @patch('src.tools.expert_tools.KnowledgeBase')
    def test_learn_new_technology(self, mock_kb, expert_tools):
        """Test learning new technology"""
        mock_instance = MagicMock()
        mock_instance.store_knowledge.return_value = 1
        mock_kb.return_value = mock_instance
        
        result = expert_tools.learn_new_technology("python", ["basics", "advanced"])
        assert isinstance(result, str)
    
    @patch('src.tools.expert_tools.KnowledgeBase')
    def test_read_knowledge_base(self, mock_kb, expert_tools):
        """Test reading from knowledge base"""
        mock_instance = MagicMock()
        mock_instance.retrieve_knowledge.return_value = [
            {'topic': 'test', 'content': 'test content', 'relevance_score': 0.9}
        ]
        mock_kb.return_value = mock_instance
        
        result = expert_tools.read_knowledge_base("python")
        assert isinstance(result, str)


class TestExtendedTools:
    """Tests for ExtendedTools class"""
    
    @pytest.fixture
    def extended_tools(self):
        """Create ExtendedTools instance"""
        return ExtendedTools()
    
    def test_extended_tools_initialization(self, extended_tools):
        """Test extended tools initializes"""
        assert extended_tools is not None
    
    def test_get_tool_descriptions(self, extended_tools):
        """Test getting tool descriptions"""
        descriptions = extended_tools.get_tool_descriptions()
        assert isinstance(descriptions, str)
        assert len(descriptions) > 0

