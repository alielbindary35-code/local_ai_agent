"""
Excel Handler
=============

Advanced Excel file handling with pandas and openpyxl:
- Reading and writing Excel files
- Data cleaning and preprocessing
- Advanced data analysis
- Format validation
- Error handling
"""

import pandas as pd
import openpyxl
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ExcelHandler:
    """
    Advanced Excel file handler with data cleaning and analysis capabilities.
    """
    
    def __init__(self):
        """Initialize Excel handler."""
        self.supported_formats = ['.xlsx', '.xls', '.xlsm']
    
    def read_excel(
        self,
        filepath: str,
        sheet_name: Optional[Union[str, int, List]] = None,
        header: int = 0,
        skiprows: Optional[int] = None,
        nrows: Optional[int] = None,
        usecols: Optional[Union[str, List]] = None
    ) -> Dict[str, Any]:
        """
        Read Excel file with comprehensive error handling.
        
        Args:
            filepath: Path to Excel file
            sheet_name: Sheet name(s) to read (None for all sheets)
            header: Row to use as column names
            skiprows: Number of rows to skip
            nrows: Number of rows to read
            usecols: Columns to read
        
        Returns:
            Dictionary with 'success', 'data' (DataFrame or dict of DataFrames), and 'metadata'
        """
        try:
            file_path = Path(filepath)
            
            # Validate file exists
            if not file_path.exists():
                return {
                    'success': False,
                    'error': f'File not found: {filepath}',
                    'data': None,
                    'metadata': {}
                }
            
            # Validate file format
            if file_path.suffix.lower() not in self.supported_formats:
                return {
                    'success': False,
                    'error': f'Unsupported file format: {file_path.suffix}. Supported: {self.supported_formats}',
                    'data': None,
                    'metadata': {}
                }
            
            # Read Excel file
            try:
                if sheet_name is None:
                    # Read all sheets
                    excel_file = pd.ExcelFile(filepath)
                    data = {}
                    for sheet in excel_file.sheet_names:
                        data[sheet] = pd.read_excel(
                            excel_file,
                            sheet_name=sheet,
                            header=header,
                            skiprows=skiprows,
                            nrows=nrows,
                            usecols=usecols
                        )
                    result_data = data
                else:
                    # Read specific sheet(s)
                    result_data = pd.read_excel(
                        filepath,
                        sheet_name=sheet_name,
                        header=header,
                        skiprows=skiprows,
                        nrows=nrows,
                        usecols=usecols
                    )
                
                # Get metadata
                metadata = {
                    'filepath': str(file_path),
                    'file_size': file_path.stat().st_size,
                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    'sheets': list(excel_file.sheet_names) if sheet_name is None else [sheet_name] if isinstance(sheet_name, str) else sheet_name
                }
                
                if isinstance(result_data, pd.DataFrame):
                    metadata.update({
                        'rows': len(result_data),
                        'columns': list(result_data.columns),
                        'column_count': len(result_data.columns)
                    })
                
                return {
                    'success': True,
                    'data': result_data,
                    'metadata': metadata,
                    'error': None
                }
                
            except Exception as e:
                logger.error(f"Error reading Excel file: {e}")
                return {
                    'success': False,
                    'error': f'Error reading Excel file: {str(e)}',
                    'data': None,
                    'metadata': {}
                }
        
        except Exception as e:
            logger.error(f"Unexpected error in read_excel: {e}")
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}',
                'data': None,
                'metadata': {}
            }
    
    def write_excel(
        self,
        filepath: str,
        data: Union[pd.DataFrame, Dict[str, pd.DataFrame]],
        sheet_name: str = 'Sheet1',
        index: bool = False,
        engine: str = 'openpyxl'
    ) -> Dict[str, Any]:
        """
        Write data to Excel file.
        
        Args:
            filepath: Output file path
            data: DataFrame or dict of DataFrames (for multiple sheets)
            sheet_name: Sheet name (if data is single DataFrame)
            index: Whether to write row indices
            engine: Excel engine ('openpyxl' or 'xlsxwriter')
        
        Returns:
            Dictionary with 'success' and 'message'
        """
        try:
            file_path = Path(filepath)
            
            # Create parent directories if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write to Excel
            if isinstance(data, pd.DataFrame):
                data.to_excel(filepath, sheet_name=sheet_name, index=index, engine=engine)
            elif isinstance(data, dict):
                with pd.ExcelWriter(filepath, engine=engine) as writer:
                    for sheet, df in data.items():
                        df.to_excel(writer, sheet_name=sheet, index=index)
            else:
                return {
                    'success': False,
                    'error': 'Data must be DataFrame or dict of DataFrames',
                    'message': None
                }
            
            return {
                'success': True,
                'message': f'Successfully wrote to {filepath}',
                'error': None
            }
        
        except Exception as e:
            logger.error(f"Error writing Excel file: {e}")
            return {
                'success': False,
                'error': f'Error writing Excel file: {str(e)}',
                'message': None
            }
    
    def clean_data(
        self,
        df: pd.DataFrame,
        remove_empty_rows: bool = True,
        remove_empty_columns: bool = True,
        fill_na: Optional[Union[str, float, int]] = None,
        remove_duplicates: bool = False,
        normalize_dates: bool = True,
        strip_strings: bool = True
    ) -> pd.DataFrame:
        """
        Clean and preprocess DataFrame.
        
        Args:
            df: Input DataFrame
            remove_empty_rows: Remove rows where all values are NaN
            remove_empty_columns: Remove columns where all values are NaN
            fill_na: Value to fill NaN with (None to skip)
            remove_duplicates: Remove duplicate rows
            normalize_dates: Convert date columns to datetime
            strip_strings: Strip whitespace from string columns
        
        Returns:
            Cleaned DataFrame
        """
        try:
            cleaned_df = df.copy()
            
            # Remove empty rows
            if remove_empty_rows:
                cleaned_df = cleaned_df.dropna(how='all')
            
            # Remove empty columns
            if remove_empty_columns:
                cleaned_df = cleaned_df.dropna(axis=1, how='all')
            
            # Fill NaN values
            if fill_na is not None:
                cleaned_df = cleaned_df.fillna(fill_na)
            
            # Remove duplicates
            if remove_duplicates:
                cleaned_df = cleaned_df.drop_duplicates()
            
            # Normalize dates
            if normalize_dates:
                for col in cleaned_df.columns:
                    if cleaned_df[col].dtype == 'object':
                        try:
                            cleaned_df[col] = pd.to_datetime(cleaned_df[col], format='mixed', errors='coerce')
                        except:
                            pass
            
            # Strip strings
            if strip_strings:
                for col in cleaned_df.columns:
                    if cleaned_df[col].dtype == 'object':
                        cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
            
            return cleaned_df
        
        except Exception as e:
            logger.error(f"Error cleaning data: {e}")
            return df
    
    def analyze_data(
        self,
        df: pd.DataFrame,
        include_stats: bool = True,
        include_correlations: bool = True,
        include_missing: bool = True
    ) -> Dict[str, Any]:
        """
        Perform statistical analysis on DataFrame.
        
        Args:
            df: Input DataFrame
            include_stats: Include descriptive statistics
            include_correlations: Include correlation matrix
            include_missing: Include missing value analysis
        
        Returns:
            Dictionary with analysis results
        """
        try:
            analysis = {
                'shape': {
                    'rows': len(df),
                    'columns': len(df.columns)
                },
                'columns': list(df.columns),
                'dtypes': df.dtypes.to_dict()
            }
            
            # Descriptive statistics
            if include_stats:
                analysis['statistics'] = df.describe().to_dict()
            
            # Correlation matrix
            if include_correlations:
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 1:
                    analysis['correlations'] = df[numeric_cols].corr().to_dict()
            
            # Missing values
            if include_missing:
                missing = df.isnull().sum()
                analysis['missing_values'] = {
                    col: int(count) for col, count in missing.items() if count > 0
                }
                analysis['missing_percentage'] = {
                    col: round((count / len(df)) * 100, 2)
                    for col, count in missing.items() if count > 0
                }
            
            return analysis
        
        except Exception as e:
            logger.error(f"Error analyzing data: {e}")
            return {'error': str(e)}
    
    def get_top_n(
        self,
        df: pd.DataFrame,
        column: str,
        n: int = 5,
        ascending: bool = False
    ) -> pd.DataFrame:
        """
        Get top N rows by column value.
        
        Args:
            df: Input DataFrame
            column: Column to sort by
            n: Number of rows to return
            ascending: Sort order
        
        Returns:
            Top N rows DataFrame
        """
        try:
            if column not in df.columns:
                raise ValueError(f"Column '{column}' not found")
            
            return df.nlargest(n, column) if not ascending else df.nsmallest(n, column)
        
        except Exception as e:
            logger.error(f"Error getting top N: {e}")
            return pd.DataFrame()

