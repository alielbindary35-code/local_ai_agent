
import sys
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.agents.expert_agent import ExpertAgent
from src.core.prompts import get_system_prompt

def test_initialization():
    print("Testing ExpertAgent Initialization...", flush=True)
    
    # Mock network calls to avoid hanging
    with patch('src.utils.connection_checker.ConnectionChecker.check_and_display', return_value=True), \
         patch('src.agents.expert_agent.requests.get') as mock_get:
        
        # Mock Ollama response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'models': [{'name': 'test-model', 'size': 1000000000}]}
        mock_get.return_value = mock_response
        
        try:
            agent = ExpertAgent()
            print("✅ ExpertAgent initialized successfully (Mocked Network)", flush=True)
            return agent
        except Exception as e:
            print(f"❌ ExpertAgent initialization failed: {e}", flush=True)
            return None

def test_prompt_generation(agent):
    print("\nTesting Prompt Generation...", flush=True)
    try:
        # Test Online Prompt
        agent.online = True
        prompt_online = agent._build_expert_prompt("Test user input", "test-model")
        
        if "ONLINE STATUS: ONLINE" in prompt_online:
            print("✅ Online status correctly reflected in prompt")
        else:
            print(f"❌ Online status missing or incorrect. Found: {prompt_online[:200]}...")

        # Test Offline Prompt
        agent.online = False
        prompt_offline = agent._build_expert_prompt("Test user input", "test-model")
        
        if "ONLINE STATUS: OFFLINE" in prompt_offline:
            print("✅ Offline status correctly reflected in prompt")
        else:
            print("❌ Offline status missing or incorrect")
            
        if "AVAILABLE TOOLS" in prompt_online:
            print("✅ Tools list included")
        
        print("✅ Prompt generation verification complete", flush=True)
        
    except Exception as e:
        print(f"❌ Prompt generation failed: {e}", flush=True)

if __name__ == "__main__":
    agent = test_initialization()
    if agent:
        test_prompt_generation(agent)
