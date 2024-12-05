"""
NFL Player Stats Parser - Data Parsing Module
"""
from typing import Dict, List
import pandas as pd
import numpy as np

class NFLStatsParser:
    """
    Parser for NFL player statistics data
    """
    
    def parse_table(self, table_data: Dict) -> pd.DataFrame:
        """
        Convert raw table data into a pandas DataFrame.
        
        Args:
            table_data: Dictionary containing headers and data rows
            
        Returns:
            Pandas DataFrame with cleaned and typed data
        """
        headers = table_data['headers']
        data = table_data['data']
        
        # Create DataFrame
        df = pd.DataFrame(data, columns=headers)
        return self.clean_data(df)
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and type the data in the DataFrame.
        
        Args:
            df: Raw DataFrame
            
        Returns:
            Cleaned DataFrame with proper types
        """
        # Make a copy to avoid modifying the original
        df = df.copy()
        
        # Handle RB-specific YACON columns
        if 'YACON' in df.columns:
            yacon_columns = [i for i, col in enumerate(df.columns) if col == 'YACON']
            if len(yacon_columns) == 2:
                # Create new column names
                new_columns = list(df.columns)
                new_columns[yacon_columns[0]] = 'YACON (Rushing)'
                new_columns[yacon_columns[1]] = 'YACON (Receiving)'
                df.columns = new_columns
        
        # Convert numeric columns
        for col in df.columns:
            if col not in ['Player', 'Team', 'Pos']:
                df[col] = self._convert_to_numeric(df[col])
        
        return df
    
    def validate_data(self, df: pd.DataFrame) -> bool:
        """
        Validate the DataFrame has required columns and proper types.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            True if valid, raises ValueError if not
        """
        # Check if DataFrame is empty first
        if df.empty:
            raise ValueError("DataFrame is empty")
            
        # Then check for required columns
        required_cols = ['Player', 'Team']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        return True
    
    def _convert_to_numeric(self, series: pd.Series) -> pd.Series:
        """Convert a series to numeric, handling percentages and special cases."""
        try:
            # If series is already numeric, return as is
            if pd.api.types.is_numeric_dtype(series):
                return series
                
            # Convert to string first to handle any non-string data
            series = series.astype(str)
            
            # Remove any '%' signs and commas
            series = series.apply(lambda x: x.replace('%', '').replace(',', '') if isinstance(x, str) else x)
            
            # Convert to numeric, setting errors to NaN
            return pd.to_numeric(series, errors='coerce')
        except Exception as e:
            # If conversion fails, try to convert directly to numeric
            try:
                return pd.to_numeric(series, errors='coerce')
            except:
                # If all else fails, return the original series
                return series

if __name__ == "__main__":
    # Example usage
    from scraper import NFLStatsScraper
    
    scraper = NFLStatsScraper()
    parser = NFLStatsParser()
    
    # Fetch and parse QB data
    html = scraper.fetch_stats('qb', 2023)
    if html:
        table_data = scraper.extract_table_data(html)
        df = parser.parse_table(table_data)
        print("\nDataFrame Info:")
        print(df.info())
        print("\nFirst few rows:")
        print(df.head()) 