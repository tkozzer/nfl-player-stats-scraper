# NFL Player Stats Scraper

A Python tool to scrape NFL player statistics from FantasyPros.com and save them in CSV or JSON format.

## Features

- Scrapes advanced stats for QB, RB, WR, and TE positions
- Supports historical data from 2013 to present
- Saves data in clean, typed CSV or JSON format
- Handles rate limiting with exponential backoff
- Validates data integrity with detailed error reporting
- Command-line interface with year selection
- Position-specific data cleaning and validation
- Format conversion between CSV and JSON
- Organized directory structure for different formats

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

To scrape data for all positions for the current year (default CSV format):

```bash
python main.py
```

To scrape data for a specific year:

```bash
python main.py 2022              # CSV format (default)
python main.py 2022 --json       # JSON format
python main.py 2022 --csv        # Explicit CSV format
```

To convert between formats:
```bash
# Convert all CSV files to JSON
python main.py --convert-to json

# Convert specific directory
python main.py --convert-to json --path output/csv

# Convert specific year
python main.py --convert-to json --year 2023

# Convert JSON back to CSV
python main.py --convert-to csv --path output/json
```

The script will:
1. Scrape data for all positions
2. Save files in the specified format
3. Validate the generated files (CSV validation only)
4. Display validation results with detailed error reporting if any issues are found

### Python API

```python
from src.writer import scrape_and_save_all
from src.validate import validate_csv
from src.converter import NFLStatsConverter

# Scrape all positions for 2023 in JSON format
results = scrape_and_save_all(2023, output_format='json')

# Convert between formats
converter = NFLStatsConverter()
results = converter.convert_files('json', path='output/csv', year=2023)
```

## Output

Data is saved in the `output/` directory with separate subdirectories for each format:

```
output/
├── csv/
│   └── 2023/
│       ├── qb_stats.csv
│       ├── rb_stats.csv
│       ├── te_stats.csv
│       └── wr_stats.csv
└── json/
    └── 2023/
        ├── qb_stats.json
        ├── rb_stats.json
        ├── te_stats.json
        └── wr_stats.json
```

### JSON Format
The JSON output maintains the same structure as CSV files, with each player's data represented as a JSON object:

```json
[
    {
        "Rank": "1",
        "Player": "Player Name",
        "Team": "Team",
        "G": "16",
        // ... additional stats specific to position
    }
]
```

## Project Structure

```
nfl-player-stats-scraper/
├── src/
│   ├── __init__.py   # Module initialization
│   ├── scraper.py    # Web scraping functionality
│   ├── parser.py     # Data parsing and cleaning
│   ├── writer.py     # File writing (CSV/JSON)
│   ├── validate.py   # Data validation
│   └── converter.py  # Format conversion
├── output/           # Generated files
│   ├── csv/         # CSV format files
│   └── json/        # JSON format files
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