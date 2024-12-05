"""
NFL Player Stats Writer - CSV and JSON Writing Module
"""
import os
import json
from pathlib import Path
import pandas as pd
from src.scraper import NFLStatsScraper
from src.parser import NFLStatsParser

class NFLStatsWriter:
    """
    Writer for NFL player statistics data
    """
    
    def __init__(self, base_dir: str = "output", output_format: str = "csv"):
        """
        Initialize writer with base output directory and format.
        
        Args:
            base_dir: Base directory for output files
            output_format: Output format ('csv' or 'json')
        """
        self.base_dir = Path(base_dir)
        self.output_format = output_format.lower()
        if self.output_format not in ['csv', 'json']:
            raise ValueError("Output format must be 'csv' or 'json'")
    
    def create_output_dir(self, year: int) -> Path:
        """
        Create output directory for the specified year if it doesn't exist.
        
        Args:
            year: Year to create directory for
            
        Returns:
            Path object for the created directory
        """
        year_dir = self.base_dir / self.output_format / str(year)
        year_dir.mkdir(parents=True, exist_ok=True)
        return year_dir
    
    def save_data(self, df: pd.DataFrame, position: str, year: int) -> str:
        """
        Save DataFrame to file in the specified format.
        
        Args:
            df: DataFrame to save
            position: Player position (qb, rb, wr, te)
            year: Season year
            
        Returns:
            Path to saved file
            
        Raises:
            TypeError: If position is not a string or year is not an integer
            AttributeError: If df is not a pandas DataFrame
        """
        # Type checking
        if not isinstance(position, str):
            raise TypeError("Position must be a string")
        if not isinstance(year, int):
            raise TypeError("Year must be an integer")
        if not isinstance(df, pd.DataFrame):
            raise AttributeError("Data must be a pandas DataFrame")
        
        # Create output directory
        output_dir = self.create_output_dir(year)
        
        # Create filename based on format
        extension = 'json' if self.output_format == 'json' else 'csv'
        filename = f"{position}_stats.{extension}"
        filepath = output_dir / filename
        
        # Save to file
        if self.output_format == 'json':
            # Convert DataFrame to list of dictionaries and save as JSON
            json_data = df.to_dict(orient='records')
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=4)
        else:
            # Save as CSV
            df.to_csv(filepath, index=False)
        
        return str(filepath)
    
    def save_to_csv(self, df: pd.DataFrame, position: str, year: int) -> str:
        """
        Legacy method for CSV saving - redirects to save_data with CSV format
        """
        old_format = self.output_format
        self.output_format = 'csv'
        result = self.save_data(df, position, year)
        self.output_format = old_format
        return result

def scrape_and_save_all(year: int, positions: list = None, output_format: str = 'csv') -> dict:
    """
    Scrape and save data for all positions for a given year.
    
    Args:
        year: Year to scrape data for
        positions: List of positions to scrape (defaults to all)
        output_format: Output format ('csv' or 'json')
        
    Returns:
        Dictionary mapping positions to their file paths
    """
    if positions is None:
        positions = ['qb', 'rb', 'wr', 'te']
    
    scraper = NFLStatsScraper()
    parser = NFLStatsParser()
    writer = NFLStatsWriter(output_format=output_format)
    
    results = {}
    
    for position in positions:
        try:
            # Fetch data
            html = scraper.fetch_stats(position, year)
            if not html:
                print(f"Failed to fetch data for {position.upper()} {year}")
                continue
            
            # Parse data
            table_data = scraper.extract_table_data(html)
            df = parser.parse_table(table_data)
            
            # Validate data
            parser.validate_data(df)
            
            # Save to file
            filepath = writer.save_data(df, position, year)
            results[position] = filepath
            print(f"Successfully saved {position.upper()} {year} data to {filepath}")
            
        except Exception as e:
            print(f"Error processing {position.upper()} {year}: {str(e)}")
    
    return results

if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        year = int(sys.argv[1])
    else:
        year = 2023
    
    results = scrape_and_save_all(year)
    print("\nSummary:")
    for position, filepath in results.items():
        print(f"{position.upper()}: {filepath}") 