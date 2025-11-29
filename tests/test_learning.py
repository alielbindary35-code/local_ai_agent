"""
Test learning functionality
"""
import os
import pytest
from src.tools.expert_tools import ExpertTools
from src.core.paths import get_knowledge_base_dir


def test_learning():
    """Test Active Learning Tool"""
    tools = ExpertTools()
    
    # Test learning new technology
    result = tools.learn_new_technology("n8n", ["Workflows", "Nodes", "Triggers"])
    assert result is not None
    assert isinstance(result, str)
    
    # Verify folder creation
    kb_dir = get_knowledge_base_dir()
    expected_path = kb_dir / "n8n"
    assert expected_path.exists(), f"Folder not found at {expected_path}"
    
    # Check if files were created
    files = list(expected_path.glob("*.md"))
    assert len(files) > 0, "No markdown files created"
