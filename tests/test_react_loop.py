import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.expert_agent import ExpertAgent

class TestReActLoop(unittest.TestCase):
    def setUp(self):
        self.agent = ExpertAgent()
        # Mock the tools to avoid actual file system changes during test
        self.agent.tools = MagicMock()
        self.agent.tools.write_file.return_value = "File created successfully."
        self.agent.expert_tools = MagicMock()
        self.agent.extended_tools = MagicMock()
        
        # Mock console to avoid clutter
        self.agent.console = MagicMock()

    @patch('src.agents.expert_agent.ExpertAgent._call_ollama')
    def test_react_loop_execution(self, mock_call_ollama):
        # Define a sequence of responses from the LLM
        # Response 1: Thought + Action
        response_1 = """
Thought: I need to create a file named test.txt.
Action: write_file
Action Input: {"filepath": "test.txt", "content": "Hello World"}
"""
        # Response 2: Final Answer (after observation)
        response_2 = """
Thought: The file has been created.
Final Answer: I have created the file test.txt with the content "Hello World".
"""
        
        # Set side_effect to return these responses in order
        mock_call_ollama.side_effect = [response_1, response_2]
        
        # Run the agent
        result = self.agent.run("Create a file named test.txt with content 'Hello World'")
        
        # Verify interactions
        # 1. Check if write_file was called
        self.agent.tools.write_file.assert_called_with(filepath="test.txt", content="Hello World")
        
        # 2. Check if final answer matches
        self.assertEqual(result, 'I have created the file test.txt with the content "Hello World".')
        
        # 3. Check if _call_ollama was called twice (once for action, once for final answer)
        self.assertEqual(mock_call_ollama.call_count, 2)
        
        print("\n✅ ReAct Loop Test Passed!")

if __name__ == '__main__':
    unittest.main()
