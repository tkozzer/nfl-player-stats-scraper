"""
NFL Player Stats Writer - CSV Writing Module
"""
import os
from pathlib import Path
import pandas as pd
from src.scraper import NFLStatsScraper
from src.parser import NFLStatsParser

class NFLStatsWriter:
    """
    Writer for NFL player statistics data
    """
    
    def __init__(self, base_dir: str = "output"):
        """
        Initialize writer with base output directory.
        
        Args:
            base_dir: Base directory for output files
        """
        self.base_dir = Path(base_dir)
    
    def create_output_dir(self, year: int) -> Path:
        """
        Create output directory for the specified year if it doesn't exist.
        
        Args:
            year: Year to create directory for
            
        Returns:
            Path object for the created directory
        """
        year_dir = self.base_dir / str(year)
        year_dir.mkdir(parents=True, exist_ok=True)
        return year_dir
    
    def save_to_csv(self, df: pd.DataFrame, position: str, year: int) -> str:
        """
        Save DataFrame to CSV file.
        
        Args:
            df: DataFrame to save
            position: Player position (qb, rb, wr, te)
            year: Season year
            
        Returns:
            Path to saved CSV file
            
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
        
        # Create filename
        filename = f"{position}_stats.csv"
        filepath = output_dir / filename
        
        # Save to CSV
        df.to_csv(filepath, index=False)
        
        return str(filepath)

def scrape_and_save_all(year: int, positions: list = None) -> dict:
    """
    Scrape and save data for all positions for a given year.
    
    Args:
        year: Year to scrape data for
        positions: List of positions to scrape (defaults to all)
        
    Returns:
        Dictionary mapping positions to their CSV file paths
    """
    if positions is None:
        positions = ['qb', 'rb', 'wr', 'te']
    
    scraper = NFLStatsScraper()
    parser = NFLStatsParser()
    writer = NFLStatsWriter()
    
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
            
            # Save to CSV
            filepath = writer.save_to_csv(df, position, year)
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