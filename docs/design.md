# NFL Player Stats Scraper - Design Document

## Project Overview
A Python-based web scraping application to collect NFL player statistics from FantasyPros.com and convert them into CSV format for consumption by other applications.

## Data Sources
- Quarterback Stats: `https://www.fantasypros.com/nfl/advanced-stats-qb.php?year={YEAR}`
- Running Back Stats: `https://www.fantasypros.com/nfl/advanced-stats-rb.php?year={YEAR}`
- Wide Receiver Stats: `https://www.fantasypros.com/nfl/advanced-stats-wr.php?year={YEAR}`
- Tight End Stats: `https://www.fantasypros.com/nfl/advanced-stats-te.php?year={YEAR}`

Year range: 2013-2024

## Technical Architecture

### 1. Core Components

#### a. Web Scraper Module
- Uses `requests` library to fetch HTML content
- Uses `BeautifulSoup4` for HTML parsing
- Implements rate limiting and exponential backoff for retries
- Handles HTTP errors with custom exceptions

#### b. Data Parser Module
- Extracts table headers and data for each position
- Normalizes data types (converts strings to appropriate numeric types)
- Handles missing or malformed data
- Validates data integrity
- Implements position-specific data cleaning rules

#### c. CSV Writer Module
- Creates position-specific CSV files
- Implements proper CSV formatting with headers
- Handles special characters and escaping
- Creates output directory if it doesn't exist
- Returns dictionary mapping positions to file paths

#### d. Validation Module
- Validates CSV files after creation
- Checks for required columns
- Verifies data types and ranges
- Reports detailed validation errors

### 2. Project Structure
```
nfl-player-stats-scraper/
├── src/
│   ├── __init__.py
│   ├── scraper.py
│   ├── parser.py
│   ├── writer.py
│   ├── validate.py
│   └── exceptions.py
├── output/
│   └── {year}/
│       ├── qb_stats.csv
│       ├── rb_stats.csv
│       ├── wr_stats.csv
│       └── te_stats.csv
├── tests/
│   ├── __init__.py
│   ├── test_scraper.py
│   ├── test_parser.py
│   ├── test_writer.py
│   └── test_validate.py
├── requirements.txt
└── README.md
```

## Implementation Details

### 1. Dependencies
- `requests`: HTTP requests
- `beautifulsoup4`: HTML parsing
- `pandas`: Data manipulation and CSV writing
- `pytest`: Testing framework
- `rich`: Console output formatting (optional)

### 2. Key Functions

#### Main
```python
def main() -> None
def scrape_and_save_all(year: int) -> dict[str, Path]
```

#### Scraper
```python
def fetch_stats(position: str, year: int) -> str
def validate_year(year: int) -> bool
def get_url(position: str, year: int) -> str
def handle_request_with_retry(url: str) -> requests.Response
```

#### Parser
```python
def parse_table(html: str, position: str) -> pd.DataFrame
def clean_data(df: pd.DataFrame, position: str) -> pd.DataFrame
def validate_data(df: pd.DataFrame, position: str) -> bool
```

#### Writer
```python
def save_to_csv(df: pd.DataFrame, position: str, year: int) -> Path
def create_output_dir(year: int) -> Path
```

#### Validator
```python
def validate_csv(filepath: Path) -> tuple[bool, list[str]]
def check_required_columns(df: pd.DataFrame, position: str) -> list[str]
def validate_data_types(df: pd.DataFrame, position: str) -> list[str]
```

### 3. Error Handling
- Custom exceptions for different error types
- Network connection errors with retry mechanism
- Invalid year ranges
- Malformed HTML responses
- Missing data fields
- File system errors
- Position-specific validation errors

### 4. Data Validation
- Year range validation (2013-2024)
- Position type validation (QB, RB, WR, TE)
- Data type validation for numeric fields
- Required field presence checking
- Post-processing CSV validation
- Detailed error reporting

## Output Format

Each position will have its own CSV file with headers specific to that position's statistics. Files are organized by year in the output directory.

Example CSV structure for QBs:
```
Player,Team,Games,Completions,Attempts,Yards,TDs,INTs,...
Patrick Mahomes,KC,16,380,584,4839,37,13,...
```

## Command Line Interface
The application accepts a year argument from the command line:
```bash
python main.py [YEAR]
```
If no year is provided, it defaults to the current season (2023).

## Future Enhancements
1. Concurrent scraping for multiple years
2. JSON output format option
3. Data visualization capabilities
4. Incremental updates for current year
5. Historical data caching
6. Configuration file for customizable settings
7. Progress bars for long-running operations
8. Logging system for debugging

## Testing Strategy
1. Unit tests for each module
2. Integration tests for full workflow
3. Mock HTTP responses for testing
4. Edge case validation
5. Performance testing for large data sets
6. Validation testing with corrupted data
7. Command line argument testing