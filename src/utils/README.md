# Utility Modules

Utility functions and helpers used throughout the system.

## Modules

### Cache Manager (`cache_manager.py`)
Manages caching for API responses and expensive operations:
- TTL-based caching
- Cache invalidation
- Persistent cache storage

**Usage:**
```python
from src.utils.cache_manager import CacheManager

cache = CacheManager()
cached_result = cache.get_or_set("key", lambda: expensive_operation())
```

### Connection Checker (`connection_checker.py`)
Network connectivity and service availability checking:
- Internet connectivity detection
- Service endpoint checking
- Connection timeout handling

**Usage:**
```python
from src.utils.connection_checker import ConnectionChecker

checker = ConnectionChecker()
is_online = checker.is_online()
is_service_available = checker.check_service("http://api.example.com")
```

## Adding New Utilities

When adding new utility modules:
1. Keep them focused on a single responsibility
2. Add comprehensive error handling
3. Include usage examples in docstrings
4. Write unit tests
5. Update this README

