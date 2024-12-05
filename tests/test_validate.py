import pytest
import os
import tempfile
from src.validate import validate_csv

@pytest.fixture
def valid_csv_file():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write("Player,Team,Pass Yds\nTom Brady,TB,4000\n")
        return f.name

@pytest.fixture
def invalid_csv_file():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write("Player,Team\nTom Brady,TB,4000\n")  # Missing header
        return f.name

@pytest.fixture
def duplicate_headers_csv():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write("Player,Team,Team\nTom Brady,TB,4000\n")
        return f.name

@pytest.fixture
def inconsistent_columns_csv():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write("Player,Team,Pass Yds\nTom Brady,TB\n")  # Missing value
        return f.name

@pytest.fixture
def empty_values_csv():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write("Player,Team,Pass Yds\nTom Brady,,4000\n")  # Empty team value
        return f.name

def test_validate_valid_csv(valid_csv_file):
    """Test validation of a valid CSV file."""
    is_valid, errors = validate_csv(valid_csv_file)
    assert is_valid
    assert len(errors) == 0
    os.unlink(valid_csv_file)

def test_validate_invalid_csv(invalid_csv_file):
    """Test validation of an invalid CSV file."""
    is_valid, errors = validate_csv(invalid_csv_file)
    assert not is_valid
    assert len(errors) > 0
    os.unlink(invalid_csv_file)

def test_validate_nonexistent_file():
    """Test validation of a non-existent file."""
    is_valid, errors = validate_csv("nonexistent.csv")
    assert not is_valid
    assert len(errors) > 0

def test_validate_duplicate_headers(duplicate_headers_csv):
    """Test validation of CSV with duplicate column headers."""
    is_valid, errors = validate_csv(duplicate_headers_csv)
    assert not is_valid
    assert any("duplicate column headers" in error.lower() for error in errors)
    os.unlink(duplicate_headers_csv)

def test_validate_inconsistent_columns(inconsistent_columns_csv):
    """Test validation of CSV with inconsistent number of columns."""
    is_valid, errors = validate_csv(inconsistent_columns_csv)
    assert not is_valid
    assert any("expected" in error.lower() for error in errors)
    os.unlink(inconsistent_columns_csv)

def test_validate_empty_values(empty_values_csv):
    """Test validation of CSV with empty values."""
    is_valid, errors = validate_csv(empty_values_csv)
    assert not is_valid
    assert any("empty value" in error.lower() for error in errors)
    os.unlink(empty_values_csv)

def test_validate_empty_file():
    """Test validation of an empty file."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        pass  # Create empty file
    
    is_valid, errors = validate_csv(f.name)
    assert not is_valid
    assert any("empty" in error.lower() for error in errors)
    os.unlink(f.name) 