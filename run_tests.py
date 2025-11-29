#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test runner script for the Local AI Agent project
"""

import sys
import os
import subprocess
from pathlib import Path

def find_project_root():
    """Find project root directory"""
    current = Path(__file__).resolve().parent
    
    # Look for project markers
    markers = ['src', 'tests', 'requirements.txt', 'README.md']
    
    while current != current.parent:
        if all((current / marker).exists() for marker in markers):
            return current
        current = current.parent
    
    # Fallback to script directory
    return Path(__file__).resolve().parent

def main():
    """Run all tests"""
    project_root = find_project_root()
    
    # Change to project root
    os.chdir(project_root)
    
    print("=" * 70)
    print("Local AI Agent - Test Suite")
    print("=" * 70)
    print(f"Project Root: {project_root}")
    print()
    
    # Check if pytest is installed
    try:
        import pytest
    except ImportError:
        print("ERROR: pytest is not installed.")
        print("Please install it with: pip install pytest pytest-cov pytest-mock")
        return 1
    
    # Run pytest with coverage
    print("Running tests with coverage...")
    print()
    
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--cov-report=xml"
    ]
    
    # Add markers if specified
    if len(sys.argv) > 1:
        if sys.argv[1] == "--unit":
            cmd.extend(["-m", "unit"])
        elif sys.argv[1] == "--integration":
            cmd.extend(["-m", "integration"])
        elif sys.argv[1] == "--fast":
            cmd.extend(["-m", "not slow"])
    
    result = subprocess.run(cmd, cwd=project_root)
    
    print()
    print("=" * 70)
    if result.returncode == 0:
        print("✅ All tests passed!")
        print()
        print("Coverage report generated in:")
        print("  - HTML: htmlcov/index.html")
        print("  - XML:  coverage.xml")
    else:
        print("❌ Some tests failed. Check output above.")
    
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())

