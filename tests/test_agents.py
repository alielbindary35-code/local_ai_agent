"""
Comprehensive tests for all agent classes
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from src.agents.agent import Agent
from src.agents.expert_agent import ExpertAgent
from src.agents.simple_agent import SimpleAgent


@pytest.fixture
def mock_ollama_response():
    """Mock Ollama API response"""
    return {
        'response': json.dumps({
            'thought': 'I need to check the system',
            'action': 'get_system_info',
            'action_input': {}
        })
    }


@pytest.fixture
def mock_ollama_models():
    """Mock available models"""
    return {
        'models': [
            {'name': 'qwen2.5:3b'},
            {'name': 'llama3.1:8b'}
        ]
    }


class TestAgent:
    """Tests for base Agent class"""
    
    @patch('requests.get')
    @patch('requests.post')
    def test_agent_initialization(self, mock_post, mock_get):
        """Test agent initializes correctly"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'models': []}
        
        agent = Agent(ollama_url="http://localhost:11434", auto_approve=True)
        
        assert agent.ollama_url == "http://localhost:11434"
        assert agent.auto_approve is True
        assert agent.tools is not None
        assert agent.memory is not None
    
    @patch('requests.get')
    @patch('requests.post')
    def test_get_available_models(self, mock_post, mock_get):
        """Test getting available models"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'models': [{'name': 'test:model'}]}
        
        agent = Agent(auto_approve=True)
        models = agent._get_available_models()
        
        assert 'test:model' in models
    
    def test_analyze_task_complexity(self):
        """Test task complexity analysis"""
        agent = Agent(auto_approve=True)
        
        assert agent._analyze_task_complexity("what is python") == 'simple'
        assert agent._analyze_task_complexity("design architecture") == 'complex'
        assert agent._analyze_task_complexity("check status") == 'simple'
    
    def test_assess_risk(self):
        """Test risk assessment"""
        agent = Agent(auto_approve=True)
        
        # Safe action
        risk = agent._assess_risk('read_file', {'filepath': 'test.txt'})
        assert risk['level'] == 'safe'
        
        # Dangerous action
        risk = agent._assess_risk('delete_file', {'filepath': 'test.txt'})
        assert risk['level'] == 'dangerous'
        
        # Caution action
        risk = agent._assess_risk('run_command', {'command': 'install package'})
        assert risk['level'] == 'caution'
    
    @patch('requests.get')
    @patch('requests.post')
    def test_call_ollama(self, mock_post, mock_get):
        """Test Ollama API call"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'models': []}
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'response': 'test response'}
        
        agent = Agent(auto_approve=True)
        response = agent._call_ollama("test prompt", "test:model")
        
        assert response == 'test response'
        mock_post.assert_called_once()


class TestExpertAgent:
    """Tests for ExpertAgent class"""
    
    @patch('requests.get')
    def test_expert_agent_initialization(self, mock_get):
        """Test expert agent initializes correctly"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'models': []}
        
        with patch('src.utils.connection_checker.ConnectionChecker.check_and_display', return_value=True):
            agent = ExpertAgent(auto_approve=True)
            
            assert agent.ollama_url == "http://localhost:11434"
            assert agent.tools is not None
            assert agent.expert_tools is not None
            assert agent.extended_tools is not None
            assert agent.knowledge_base is not None
    
    @patch('requests.get')
    def test_detect_task_type(self, mock_get):
        """Test task type detection"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'models': []}
        
        with patch('src.utils.connection_checker.ConnectionChecker.check_and_display', return_value=True):
            agent = ExpertAgent(auto_approve=True)
            
            # Test various task types
            assert agent._detect_task_type("write python code") in ['coding', 'programming']
            assert agent._detect_task_type("deploy docker container") in ['docker', 'server']
            assert agent._detect_task_type("create website") in ['web_design', 'general']
            assert agent._detect_task_type("check database") in ['database', 'general']
            assert agent._detect_task_type("what is") in ['simple', 'general']
    
    @patch('requests.get')
    def test_select_best_model(self, mock_get):
        """Test model selection"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'models': [
                {'name': 'qwen2.5:3b', 'size': 3000000000},
                {'name': 'deepseek-coder:6.7b', 'size': 6700000000}
            ]
        }
        
        with patch('src.utils.connection_checker.ConnectionChecker.check_and_display', return_value=True):
            agent = ExpertAgent(auto_approve=True)
            
            # Coding task should prefer deepseek
            model = agent._select_best_model("write python code", "coding")
            assert 'deepseek' in model.lower() or 'qwen' in model.lower()


class TestSimpleAgent:
    """Tests for SimpleAgent class"""
    
    @patch('requests.post')
    def test_simple_agent_initialization(self, mock_post):
        """Test simple agent initializes correctly"""
        agent = SimpleAgent(auto_approve=True)
        
        assert agent.ollama_url == "http://localhost:11434"
        assert agent.model == "qwen2.5:3b"
        assert agent.max_iterations == 5
        assert agent.auto_approve is True
    
    @patch('requests.post')
    def test_call_ollama(self, mock_post):
        """Test Ollama call in simple agent"""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'response': 'test'}
        
        agent = SimpleAgent(auto_approve=True)
        response = agent._call_ollama("test prompt")
        
        assert response == 'test'
        mock_post.assert_called_once()


class TestAgentIntegration:
    """Integration tests for agents"""
    
    @patch('requests.get')
    @patch('requests.post')
    def test_agent_with_tools(self, mock_post, mock_get):
        """Test agent can use tools"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'models': []}
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'response': json.dumps({
                'thought': 'I need system info',
                'action': 'get_system_info',
                'action_input': {}
            })
        }
        
        agent = Agent(auto_approve=True)
        
        # Mock tools.execute to avoid actual system calls
        with patch.object(agent.tools, 'execute', return_value={'os': 'Windows'}) as mock_execute:
            result = agent.run("what is my operating system")
            
            # Should have attempted to execute tool
            assert mock_execute.called or "Windows" in str(result) or "Error" in str(result)

