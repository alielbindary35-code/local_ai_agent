"""
Test reading Docker knowledge base
"""
import pytest
from src.core.knowledge_base import KnowledgeBase


def test_read_docker():
    """Test reading Docker knowledge"""
    kb = KnowledgeBase()
    result = kb.retrieve_knowledge("Docker", limit=5)
    assert isinstance(result, list)

