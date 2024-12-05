# NFL Player Stats Scraper

A Python tool to scrape NFL player statistics from FantasyPros.com and save them in CSV format.

## Features

- Scrapes advanced stats for QB, RB, WR, and TE positions
- Supports historical data from 2013 to present
- Saves data in clean, typed CSV format
- Handles rate limiting with exponential backoff
- Validates data integrity with detailed error reporting
- Command-line interface with year selection
- Position-specific data cleaning and validation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nfl-player-stats-scraper.git
cd nfl-player-stats-scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

To scrape data for all positions for the current year:

```bash
python main.py
```

To scrape data for a specific year:

```bash
python main.py 2022
```

The script will:
1. Scrape data for all positions
2. Save CSV files in the output directory
3. Validate the generated files
4. Display validation results with detailed error reporting if any issues are found

### Python API

```python
from src.writer import scrape_and_save_all
from src.validate import validate_csv

# Scrape all positions for 2023
results = scrape_and_save_all(2023)

# Validate the generated files
for position, filepath in results.items():
    is_valid, errors = validate_csv(filepath)
    if not is_valid:
        print(f"Validation errors in {position}:", errors)
```

## Output

Data is saved in the `output/{year}/` directory with separate CSV files for each position:
- `qb_stats.csv`
- `rb_stats.csv`
- `wr_stats.csv`
- `te_stats.csv`

### Validation

The script performs several validation checks on the generated files:
- Required columns presence
- Data type validation
- Value range checks
- Position-specific validations

If any validation errors are found, they will be displayed with detailed information about the issue.

## Project Structure

```
nfl-player-stats-scraper/
├── src/
│   ├── __init__.py   # Module initialization
│   ├── scraper.py    # Web scraping functionality
│   ├── parser.py     # Data parsing and cleaning
│   ├── writer.py     # CSV file handling
│   └── validate.py   # Data validation
├── output/           # Generated CSV files
├── tests/           # Test suite
└── main.py         # Command-line interface
```

## Error Handling

The scraper includes robust error handling for:
- Network connection issues with retry mechanism
- Invalid year ranges
- Malformed HTML responses
- Missing or invalid data
- File system errors
- Position-specific validation errors

## Tests

The project includes a comprehensive test suite to ensure reliability and correctness:

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=src

# Run specific test file
pytest tests/test_scraper.py
```

### Test Structure

```
tests/
├── __init__.py
├── conftest.py          # Shared test fixtures
├── test_scraper.py      # Tests for web scraping
├── test_parser.py       # Tests for data parsing
├── test_writer.py       # Tests for file operations
└── test_validate.py     # Tests for data validation
```

### Test Coverage

Tests cover:
- Web scraping functionality and error handling
- Data parsing and cleaning operations
- CSV file writing and reading
- Data validation rules
- Edge cases and error conditions
- Integration tests for full workflow

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 