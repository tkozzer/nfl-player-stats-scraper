import pytest
import os
import tempfile
import pandas as pd
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.writer import NFLStatsWriter, scrape_and_save_all

@pytest.fixture
def writer():
    return NFLStatsWriter()

@pytest.fixture
def sample_data():
    return pd.DataFrame([
        {"Player": "Tom Brady", "Team": "TB", "Pass Yds": "4000"},
        {"Player": "Aaron Rodgers", "Team": "GB", "Pass Yds": "3800"}
    ])

def test_writer_initialization():
    """Test writer initialization with default and custom base directory."""
    # Test default initialization
    writer = NFLStatsWriter()
    assert writer.base_dir == Path("output")
    
    # Test custom base directory
    custom_writer = NFLStatsWriter("custom_dir")
    assert custom_writer.base_dir == Path("custom_dir")

def test_create_output_dir(writer):
    """Test creation of output directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        writer.base_dir = Path(tmpdir)
        year_dir = writer.create_output_dir(2023)
        assert os.path.exists(year_dir)
        assert str(year_dir).endswith("2023")

def test_save_to_csv(writer, sample_data):
    """Test saving data to CSV file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        writer.base_dir = Path(tmpdir)
        
        # Save data
        filepath = writer.save_to_csv(sample_data, "qb", 2023)
        
        # Verify file exists and contains correct data
        assert os.path.exists(filepath)
        
        # Read back and verify contents
        df = pd.read_csv(filepath)
        assert len(df) == 2
        assert "Tom Brady" in df["Player"].values
        assert "Aaron Rodgers" in df["Player"].values
        assert "Pass Yds" in df.columns

def test_save_to_csv_file_structure(writer, sample_data):
    """Test the complete file path structure when saving CSV."""
    with tempfile.TemporaryDirectory() as tmpdir:
        writer.base_dir = Path(tmpdir)
        
        # Test different positions and years
        positions = ["qb", "rb", "wr", "te"]
        years = [2022, 2023]
        
        for position in positions:
            for year in years:
                filepath = writer.save_to_csv(sample_data, position, year)
                
                # Check file path structure
                assert str(filepath).endswith(f"{position}_stats.csv")
                assert str(year) in str(filepath)
                assert os.path.exists(filepath)

@patch('src.writer.NFLStatsScraper')
@patch('src.writer.NFLStatsParser')
def test_scrape_and_save_all(mock_parser_class, mock_scraper_class):
    """Test the scrape_and_save_all function."""
    # Setup mocks
    mock_scraper = MagicMock()
    mock_parser = MagicMock()
    mock_scraper_class.return_value = mock_scraper
    mock_parser_class.return_value = mock_parser
    
    # Mock the necessary return values
    mock_scraper.fetch_stats.return_value = "<html>mock data</html>"
    mock_scraper.extract_table_data.return_value = {"headers": [], "data": []}
    mock_parser.parse_table.return_value = pd.DataFrame({"Player": [], "Team": []})
    mock_parser.validate_data.return_value = True
    
    # Test with specific positions
    with tempfile.TemporaryDirectory() as tmpdir:
        results = scrape_and_save_all(2023, positions=["qb", "rb"])
        
        # Verify results
        assert len(results) == 2
        assert "qb" in results
        assert "rb" in results
        
        # Verify scraper and parser were called correctly
        assert mock_scraper.fetch_stats.call_count == 2
        assert mock_parser.parse_table.call_count == 2
        assert mock_parser.validate_data.call_count == 2

def test_save_to_csv_error_handling(writer):
    """Test error handling when saving CSV files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        writer.base_dir = Path(tmpdir)
        
        # Test with invalid DataFrame
        with pytest.raises(AttributeError):
            writer.save_to_csv(None, "qb", 2023)
        
        # Test with invalid position type
        with pytest.raises(TypeError):
            writer.save_to_csv(pd.DataFrame(), None, 2023)
        
        # Test with invalid year type
        with pytest.raises(TypeError):
            writer.save_to_csv(pd.DataFrame(), "qb", "2023")