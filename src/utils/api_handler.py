"""
Modular API Handler
===================

A reusable, modular API handler with:
- Authentication management
- Retry logic with exponential backoff
- Error handling and logging
- Data formatting and standardization
- Request/response caching
"""

import requests
import json
import time
import logging
from typing import Dict, Any, Optional, Callable, List
from functools import wraps
from datetime import datetime, timedelta

from src.utils.cache_manager import CacheManager

# Configure logging
logger = logging.getLogger(__name__)


class APIHandler:
    """
    Modular API handler with authentication, retry logic, and error handling.
    
    Features:
    - Multiple authentication methods (API key, OAuth, Basic Auth)
    - Automatic retry with exponential backoff
    - Request/response logging
    - Data formatting and validation
    - Caching support
    """
    
    def __init__(
        self,
        base_url: Optional[str] = None,
        default_timeout: int = 30,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        enable_cache: bool = True,
        cache_ttl: int = 3600
    ):
        """
        Initialize API handler.
        
        Args:
            base_url: Base URL for API requests
            default_timeout: Default request timeout in seconds
            max_retries: Maximum number of retry attempts
            retry_delay: Initial delay between retries (seconds)
            enable_cache: Enable response caching
            cache_ttl: Cache time-to-live in seconds
        """
        self.base_url = base_url.rstrip('/') if base_url else None
        self.default_timeout = default_timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.session = requests.Session()
        self.auth_config = {}
        self.cache_manager = CacheManager() if enable_cache else None
        self.cache_ttl = cache_ttl
        
        # Default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'AI-Agent/1.0'
        })
    
    def set_auth_api_key(self, api_key: str, header_name: str = 'X-API-Key'):
        """
        Set API key authentication.
        
        Args:
            api_key: API key value
            header_name: Header name for API key
        """
        self.auth_config = {
            'type': 'api_key',
            'key': api_key,
            'header': header_name
        }
        self.session.headers[header_name] = api_key
        logger.info(f"API key authentication configured (header: {header_name})")
    
    def set_auth_basic(self, username: str, password: str):
        """
        Set basic authentication.
        
        Args:
            username: Username
            password: Password
        """
        self.auth_config = {
            'type': 'basic',
            'username': username,
            'password': password
        }
        self.session.auth = (username, password)
        logger.info("Basic authentication configured")
    
    def set_auth_bearer(self, token: str):
        """
        Set bearer token authentication.
        
        Args:
            token: Bearer token
        """
        self.auth_config = {
            'type': 'bearer',
            'token': token
        }
        self.session.headers['Authorization'] = f'Bearer {token}'
        logger.info("Bearer token authentication configured")
    
    def set_auth_oauth2(self, token: str, token_type: str = 'Bearer'):
        """
        Set OAuth2 authentication.
        
        Args:
            token: OAuth2 access token
            token_type: Token type (usually 'Bearer')
        """
        self.auth_config = {
            'type': 'oauth2',
            'token': token,
            'token_type': token_type
        }
        self.session.headers['Authorization'] = f'{token_type} {token}'
        logger.info("OAuth2 authentication configured")
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[int] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Make HTTP request with retry logic.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint (relative to base_url)
            params: URL parameters
            data: Form data
            json_data: JSON data
            headers: Additional headers
            timeout: Request timeout
            use_cache: Whether to use cache for GET requests
        
        Returns:
            Response dictionary with status_code, data, and metadata
        """
        # Build full URL
        if self.base_url:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
        else:
            url = endpoint
        
        # Check cache for GET requests
        if method.upper() == 'GET' and use_cache and self.cache_manager:
            cache_key = f"api_request:{method}:{url}:{json.dumps(params or {}, sort_keys=True)}"
            cached_response = self.cache_manager.get(cache_key)
            if cached_response:
                logger.debug(f"Cache hit for {url}")
                return cached_response
        
        # Prepare request
        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)
        
        request_timeout = timeout or self.default_timeout
        
        # Retry logic
        last_exception = None
        for attempt in range(self.max_retries + 1):
            try:
                # Make request
                response = self.session.request(
                    method=method.upper(),
                    url=url,
                    params=params,
                    data=data,
                    json=json_data,
                    headers=request_headers,
                    timeout=request_timeout
                )
                
                # Process response
                result = self._process_response(response)
                
                # Cache successful GET responses
                if method.upper() == 'GET' and result['success'] and use_cache and self.cache_manager:
                    cache_key = f"api_request:{method}:{url}:{json.dumps(params or {}, sort_keys=True)}"
                    self.cache_manager.set(cache_key, result, ttl=self.cache_ttl)
                
                return result
                
            except requests.exceptions.Timeout as e:
                last_exception = e
                logger.warning(f"Request timeout (attempt {attempt + 1}/{self.max_retries + 1}): {url}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * (2 ** attempt))  # Exponential backoff
                else:
                    return {
                        'success': False,
                        'error': 'Request timeout',
                        'status_code': None,
                        'data': None,
                        'metadata': {'attempts': attempt + 1}
                    }
            
            except requests.exceptions.ConnectionError as e:
                last_exception = e
                logger.warning(f"Connection error (attempt {attempt + 1}/{self.max_retries + 1}): {url}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * (2 ** attempt))
                else:
                    return {
                        'success': False,
                        'error': 'Connection error',
                        'status_code': None,
                        'data': None,
                        'metadata': {'attempts': attempt + 1}
                    }
            
            except Exception as e:
                last_exception = e
                logger.error(f"Unexpected error (attempt {attempt + 1}/{self.max_retries + 1}): {str(e)}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * (2 ** attempt))
                else:
                    return {
                        'success': False,
                        'error': str(e),
                        'status_code': None,
                        'data': None,
                        'metadata': {'attempts': attempt + 1}
                    }
        
        # If we get here, all retries failed
        return {
            'success': False,
            'error': f'Max retries exceeded: {str(last_exception)}',
            'status_code': None,
            'data': None,
            'metadata': {'attempts': self.max_retries + 1}
        }
    
    def _process_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Process HTTP response and standardize format.
        
        Args:
            response: requests.Response object
        
        Returns:
            Standardized response dictionary
        """
        result = {
            'success': response.status_code < 400,
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'metadata': {
                'url': response.url,
                'elapsed_time': response.elapsed.total_seconds(),
                'timestamp': datetime.now().isoformat()
            }
        }
        
        # Parse response data
        try:
            content_type = response.headers.get('content-type', '').lower()
            if 'application/json' in content_type:
                result['data'] = response.json()
            else:
                result['data'] = response.text
        except Exception as e:
            logger.warning(f"Error parsing response: {e}")
            result['data'] = response.text
        
        # Add error information if request failed
        if not result['success']:
            result['error'] = f"HTTP {response.status_code}"
            if isinstance(result['data'], dict) and 'error' in result['data']:
                result['error'] = result['data']['error']
            elif isinstance(result['data'], str):
                result['error'] = result['data'][:200]  # Limit error message length
        
        return result
    
    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """Make GET request."""
        return self._make_request('GET', endpoint, params=params, **kwargs)
    
    def post(self, endpoint: str, json_data: Optional[Dict] = None, data: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """Make POST request."""
        return self._make_request('POST', endpoint, json_data=json_data, data=data, **kwargs)
    
    def put(self, endpoint: str, json_data: Optional[Dict] = None, data: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """Make PUT request."""
        return self._make_request('PUT', endpoint, json_data=json_data, data=data, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make DELETE request."""
        return self._make_request('DELETE', endpoint, **kwargs)
    
    def patch(self, endpoint: str, json_data: Optional[Dict] = None, data: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """Make PATCH request."""
        return self._make_request('PATCH', endpoint, json_data=json_data, data=data, **kwargs)
    
    def format_response_as_dataframe(self, response: Dict[str, Any]) -> Optional[Any]:
        """
        Format API response as pandas DataFrame.
        
        Args:
            response: API response dictionary
        
        Returns:
            pandas DataFrame or None if conversion fails
        """
        try:
            import pandas as pd
            
            data = response.get('data')
            if data is None:
                return None
            
            # Handle different data structures
            if isinstance(data, list):
                return pd.DataFrame(data)
            elif isinstance(data, dict):
                # Try to find list of records
                for key, value in data.items():
                    if isinstance(value, list) and len(value) > 0:
                        if isinstance(value[0], dict):
                            return pd.DataFrame(value)
                # If no list found, convert dict to DataFrame
                return pd.DataFrame([data])
            else:
                return None
                
        except ImportError:
            logger.warning("pandas not available for DataFrame conversion")
            return None
        except Exception as e:
            logger.error(f"Error converting to DataFrame: {e}")
            return None
    
    def clear_cache(self):
        """Clear API response cache."""
        if self.cache_manager:
            self.cache_manager.clear()
            logger.info("API cache cleared")
    
    def close(self):
        """Close session and cleanup."""
        self.session.close()
        logger.info("API handler closed")

