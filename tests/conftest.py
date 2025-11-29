"""
Pytest configuration and shared fixtures
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def project_root_path():
    """Get project root path"""
    return Path(__file__).parent.parent


@pytest.fixture(autouse=True)
def reset_imports():
    """Reset imports between tests"""
    yield
    # Cleanup if needed


@pytest.fixture
def mock_ollama_available():
    """Mock Ollama as available"""
    import requests
    from unittest.mock import patch
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'models': [{'name': 'qwen2.5:3b'}]
        }
        yield mock_get

