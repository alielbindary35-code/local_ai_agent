# Testing Guide

## Overview

This project includes a comprehensive test suite covering all major components of the Local AI Agent system.

## Running Tests

### Quick Start

```bash
# Run all tests
python run_tests.py

# Or use pytest directly
pytest

# Run with coverage report
pytest --cov=src --cov-report=html
```

### Test Categories

Tests are organized by component:

- **Unit Tests**: Test individual functions and classes
  - `test_agents.py` - Agent classes (Agent, ExpertAgent, SimpleAgent)
  - `test_tools.py` - Tool libraries (Tools, ExpertTools, ExtendedTools)
  - `test_memory.py` - Memory system
  - `test_knowledge_base.py` - Knowledge base system
  - `test_core_components.py` - Core utilities (paths, prompts, state_manager)
  - `test_utils.py` - Utility modules (connection_checker, cache_manager, etc.)

- **Integration Tests**: Test component interactions
  - Tests in `test_agents.py` include integration tests
  - Tests verify agents can use tools correctly

### Running Specific Tests

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run specific test file
pytest tests/test_memory.py

# Run specific test
pytest tests/test_memory.py::TestMemory::test_save_solution

# Run fast tests (skip slow ones)
pytest -m "not slow"
```

### Test Coverage

Generate coverage reports:

```bash
# Terminal report
pytest --cov=src --cov-report=term-missing

# HTML report (opens in browser)
pytest --cov=src --cov-report=html
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html  # Windows

# XML report (for CI/CD)
pytest --cov=src --cov-report=xml
```

## Test Structure

### Fixtures

Common fixtures are defined in `tests/conftest.py`:
- `project_root_path` - Project root directory
- `temp_dir` - Temporary directory for file operations
- `temp_db` - Temporary database for testing
- `mock_ollama_available` - Mock Ollama API

### Test Organization

Each test file follows this structure:

```python
class TestComponent:
    """Tests for Component class"""
    
    @pytest.fixture
    def component(self):
        """Create component instance"""
        return Component()
    
    def test_feature(self, component):
        """Test specific feature"""
        # Test implementation
        assert result == expected
```

## Writing New Tests

### Guidelines

1. **Test names**: Use descriptive names like `test_feature_scenario`
2. **Isolation**: Each test should be independent
3. **Fixtures**: Use fixtures for common setup
4. **Mocking**: Mock external dependencies (Ollama, file system, etc.)
5. **Assertions**: Use clear assertions with helpful messages

### Example Test

```python
def test_read_file_success(tools, temp_dir):
    """Test reading a file successfully"""
    test_file = Path(temp_dir) / "test.txt"
    test_file.write_text("Hello, World!")
    
    result = tools.read_file(str(test_file))
    assert "Hello, World!" in result
```

## Continuous Integration

Tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest --cov=src --cov-report=xml
    
- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## Test Requirements

All test dependencies are in `requirements.txt`:
- `pytest>=7.4.0` - Test framework
- `pytest-cov>=4.1.0` - Coverage plugin
- `pytest-mock>=3.12.0` - Mocking utilities

## Troubleshooting

### Tests Fail with Import Errors

Make sure you're running from the project root:
```bash
cd /path/to/local_ai_agent
pytest
```

### Ollama Connection Errors

Tests that require Ollama are marked with `@pytest.mark.requires_ollama`.
Mock Ollama in unit tests to avoid connection requirements.

### Database Lock Errors

Tests use temporary databases. If you see lock errors:
- Ensure tests complete properly
- Check for leftover test databases
- Use `tempfile` fixtures properly

## Coverage Goals

- **Unit Tests**: 80%+ coverage
- **Integration Tests**: Cover all major workflows
- **Critical Paths**: 100% coverage for error handling

## Contributing

When adding new features:
1. Write tests first (TDD approach)
2. Ensure all tests pass
3. Maintain or improve coverage
4. Update this guide if needed

