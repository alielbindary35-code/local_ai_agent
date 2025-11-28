"""
Unit tests for Excel Handler
"""

import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import Mock, patch
from src.utils.excel_handler import ExcelHandler


class TestExcelHandler:
    """Test cases for ExcelHandler class."""
    
    def test_init(self):
        """Test Excel handler initialization."""
        handler = ExcelHandler()
        assert handler.supported_formats == ['.xlsx', '.xls', '.xlsm']
    
    def test_read_excel_file_not_found(self):
        """Test reading non-existent Excel file."""
        handler = ExcelHandler()
        result = handler.read_excel("nonexistent.xlsx")
        
        assert result['success'] is False
        assert 'not found' in result['error'].lower()
    
    def test_read_excel_unsupported_format(self):
        """Test reading unsupported file format."""
        handler = ExcelHandler()
        # Create a dummy file with wrong extension
        test_file = Path("test.txt")
        test_file.write_text("test")
        
        result = handler.read_excel("test.txt")
        test_file.unlink()  # Cleanup
        
        assert result['success'] is False
        assert 'unsupported' in result['error'].lower()
    
    def test_clean_data(self):
        """Test data cleaning functionality."""
        handler = ExcelHandler()
        
        # Create test DataFrame with empty values
        df = pd.DataFrame({
            'A': [1, 2, None, 4],
            'B': ['a', '  b  ', None, 'd'],
            'C': [None, None, None, None]
        })
        
        cleaned = handler.clean_data(
            df,
            remove_empty_rows=True,
            remove_empty_columns=True,
            strip_strings=True
        )
        
        assert len(cleaned) <= len(df)
        assert 'C' not in cleaned.columns  # Empty column removed
    
    def test_analyze_data(self):
        """Test data analysis functionality."""
        handler = ExcelHandler()
        
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [10, 20, 30, 40, 50],
            'C': ['a', 'b', 'c', 'd', 'e']
        })
        
        analysis = handler.analyze_data(df)
        
        assert 'shape' in analysis
        assert analysis['shape']['rows'] == 5
        assert analysis['shape']['columns'] == 3
        assert 'statistics' in analysis
    
    def test_get_top_n(self):
        """Test getting top N rows."""
        handler = ExcelHandler()
        
        df = pd.DataFrame({
            'value': [10, 50, 30, 20, 40]
        })
        
        top_3 = handler.get_top_n(df, 'value', n=3)
        
        assert len(top_3) == 3
        assert top_3.iloc[0]['value'] == 50  # Highest value
    
    def test_write_excel(self, tmp_path):
        """Test writing Excel file."""
        handler = ExcelHandler()
        
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': ['a', 'b', 'c']
        })
        
        filepath = tmp_path / "test.xlsx"
        result = handler.write_excel(str(filepath), df)
        
        assert result['success'] is True
        assert filepath.exists()

