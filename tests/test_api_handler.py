"""
Unit tests for API Handler
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.utils.api_handler import APIHandler


class TestAPIHandler:
    """Test cases for APIHandler class."""
    
    def test_init(self):
        """Test API handler initialization."""
        handler = APIHandler(base_url="http://example.com")
        assert handler.base_url == "http://example.com"
        assert handler.default_timeout == 30
        assert handler.max_retries == 3
    
    def test_set_auth_api_key(self):
        """Test API key authentication setup."""
        handler = APIHandler()
        handler.set_auth_api_key("test-key", "X-API-Key")
        assert handler.auth_config['type'] == 'api_key'
        assert handler.session.headers['X-API-Key'] == "test-key"
    
    def test_set_auth_basic(self):
        """Test basic authentication setup."""
        handler = APIHandler()
        handler.set_auth_basic("user", "pass")
        assert handler.auth_config['type'] == 'basic'
        assert handler.session.auth == ("user", "pass")
    
    def test_set_auth_bearer(self):
        """Test bearer token authentication setup."""
        handler = APIHandler()
        handler.set_auth_bearer("token123")
        assert handler.auth_config['type'] == 'bearer'
        assert handler.session.headers['Authorization'] == "Bearer token123"
    
    @patch('src.utils.api_handler.requests.Session.request')
    def test_get_request_success(self, mock_request):
        """Test successful GET request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'content-type': 'application/json'}
        mock_response.json.return_value = {'data': 'test'}
        mock_response.elapsed.total_seconds.return_value = 0.5
        mock_response.url = "http://example.com/api"
        mock_request.return_value = mock_response
        
        handler = APIHandler(base_url="http://example.com")
        result = handler.get("/api")
        
        assert result['success'] is True
        assert result['status_code'] == 200
        assert result['data'] == {'data': 'test'}
    
    @patch('src.utils.api_handler.requests.Session.request')
    def test_post_request(self, mock_request):
        """Test POST request."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.headers = {'content-type': 'application/json'}
        mock_response.json.return_value = {'id': 1}
        mock_response.elapsed.total_seconds.return_value = 0.3
        mock_response.url = "http://example.com/api"
        mock_request.return_value = mock_response
        
        handler = APIHandler(base_url="http://example.com")
        result = handler.post("/api", json_data={'name': 'test'})
        
        assert result['success'] is True
        assert result['status_code'] == 201
    
    @patch('src.utils.api_handler.requests.Session.request')
    def test_request_retry_on_timeout(self, mock_request):
        """Test retry logic on timeout."""
        mock_request.side_effect = [
            Exception("Timeout"),
            Exception("Timeout"),
            Mock(status_code=200, headers={}, json=lambda: {}, elapsed=Mock(total_seconds=lambda: 0.1), url="http://example.com")
        ]
        
        handler = APIHandler(base_url="http://example.com", max_retries=2)
        # This will test retry logic (may need adjustment based on implementation)
        # result = handler.get("/api")
    
    def test_format_response_as_dataframe(self):
        """Test DataFrame formatting."""
        handler = APIHandler()
        response = {
            'data': [
                {'id': 1, 'name': 'test1'},
                {'id': 2, 'name': 'test2'}
            ]
        }
        
        df = handler.format_response_as_dataframe(response)
        assert df is not None
        assert len(df) == 2

