# Tests

This directory contains all test files for the AI agent system.

## Test Structure

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test component interactions
- **Performance Tests**: Test system performance under load

## Running Tests

### Using pytest (Recommended)
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_memory.py

# Run with coverage
pytest --cov=src tests/
```

### Using Python directly
```bash
python -m pytest tests/
```

## Test Files

- `test_memory.py`: Memory system tests
- `test_react_loop.py`: ReAct loop tests
- `test_tools.py`: Tool execution tests
- `test_api_handler.py`: API handler tests
- `test_excel_handler.py`: Excel handling tests
- `test_n8n_integration.py`: n8n integration tests

## Writing Tests

Follow these guidelines:
1. Use descriptive test names: `test_function_name_scenario`
2. Test both success and failure cases
3. Use fixtures for common setup
4. Mock external dependencies
5. Keep tests isolated and independent

## Test Coverage

Aim for:
- **Unit tests**: 80%+ coverage
- **Integration tests**: Cover all major workflows
- **Performance tests**: Test with realistic data sizes

