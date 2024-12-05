import pytest
import pandas as pd
import numpy as np
from src.parser import NFLStatsParser

@pytest.fixture
def parser():
    return NFLStatsParser()

@pytest.fixture
def sample_table_data():
    return {
        "headers": ["Player", "Team", "Pass Yds", "Cmp%", "TD"],
        "data": [
            ["Tom Brady", "TB", "4,000", "65.2%", "30"],
            ["Aaron Rodgers", "GB", "3,800", "67.3%", "35"]
        ]
    }

@pytest.fixture
def rb_table_data():
    """Special case for RB data with duplicate YACON columns"""
    return {
        "headers": ["Player", "Team", "Rush Yds", "YACON", "YACON"],
        "data": [
            ["Derrick Henry", "TEN", "1,500", "800", "200"],
            ["Dalvin Cook", "MIN", "1,200", "700", "150"]
        ]
    }

def test_parser_initialization(parser):
    """Test that parser initializes correctly."""
    assert isinstance(parser, NFLStatsParser)

def test_parse_table(parser, sample_table_data):
    """Test parsing table data with standard stats."""
    df = parser.parse_table(sample_table_data)
    
    # Check basic structure
    assert len(df) == 2
    assert list(df.columns) == ["Player", "Team", "Pass Yds", "Cmp%", "TD"]
    
    # Check data types and cleaning
    assert df["Pass Yds"].dtype in [np.float64, np.int64]
    assert df["Cmp%"].dtype in [np.float64, np.int64]
    assert df["TD"].dtype in [np.float64, np.int64]
    
    # Check specific values
    assert df["Pass Yds"].iloc[0] == 4000
    assert df["Cmp%"].iloc[0] == 65.2
    assert df["TD"].iloc[0] == 30

def test_parse_rb_data(parser, rb_table_data):
    """Test parsing RB data with duplicate YACON columns."""
    df = parser.parse_table(rb_table_data)
    
    # Check YACON column renaming
    assert "YACON (Rushing)" in df.columns
    assert "YACON (Receiving)" in df.columns
    assert "YACON" not in df.columns
    
    # Check values
    assert df["YACON (Rushing)"].iloc[0] == 800
    assert df["YACON (Receiving)"].iloc[0] == 200

def test_clean_data(parser):
    """Test data cleaning functionality."""
    # Create test data with various formats
    df = pd.DataFrame({
        "Player": ["Tom Brady", "Aaron Rodgers"],
        "Team": ["TB", "GB"],
        "Pass Yds": ["4,000", "3,800"],
        "Cmp%": ["65.2%", "67.3%"],
        "TD": ["30", "35"],
        "Rating": ["104.3", "98.6"]
    })
    
    cleaned_df = parser.clean_data(df)
    
    # Check numeric conversions
    assert cleaned_df["Pass Yds"].dtype in [np.float64, np.int64]
    assert cleaned_df["Cmp%"].dtype in [np.float64, np.int64]
    assert cleaned_df["Rating"].dtype in [np.float64, np.int64]
    
    # Check string columns remain strings
    assert cleaned_df["Player"].dtype == object
    assert cleaned_df["Team"].dtype == object

def test_validate_data(parser, sample_table_data):
    """Test data validation."""
    df = parser.parse_table(sample_table_data)
    assert parser.validate_data(df) is True
    
    # Test missing required columns
    df_missing = df.drop(columns=["Player"])
    with pytest.raises(ValueError, match="Missing required columns"):
        parser.validate_data(df_missing)
    
    # Test empty DataFrame
    with pytest.raises(ValueError, match="DataFrame is empty"):
        parser.validate_data(pd.DataFrame())

def test_numeric_conversion_edge_cases(parser):
    """Test numeric conversion with edge cases."""
    df = pd.DataFrame({
        "Player": ["Tom Brady"],
        "Team": ["TB"],
        "Pass Yds": ["N/A"],  # Non-numeric value
        "Cmp%": [""],        # Empty string
        "TD": ["30.5"]       # Decimal number
    })
    
    cleaned_df = parser.clean_data(df)
    
    # Check handling of non-numeric and empty values
    assert pd.isna(cleaned_df["Pass Yds"].iloc[0])
    assert pd.isna(cleaned_df["Cmp%"].iloc[0])
    assert cleaned_df["TD"].iloc[0] == 30.5