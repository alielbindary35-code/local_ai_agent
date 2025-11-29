"""
Test knowledge recall functionality
"""
import pytest
from src.tools.expert_tools import ExpertTools


def test_recall():
    """Test Knowledge Recall"""
    tools = ExpertTools()
    
    # Try to read knowledge (if exists)
    # Note: read_knowledge_base might not exist, use retrieve_knowledge instead
    from src.core.knowledge_base import KnowledgeBase
    kb = KnowledgeBase()
    
    result = kb.retrieve_knowledge("n8n", limit=5)
    assert isinstance(result, list)
