# JSON Output Feature Design

## Overview
This document outlines the design for adding JSON output capability to the NFL player stats scraper. The feature will allow users to choose between CSV (default) and JSON output formats through command-line arguments, as well as convert existing files between formats.

## Command-Line Interface
The program will accept new optional arguments to specify the output format and conversion operations:

```bash
# Scraping and saving in specific format
python main.py 2023 --json  # For JSON output
python main.py 2023 --csv   # For CSV output (or no argument for default CSV)

# Converting existing files
python main.py --convert-to json --path output     # Convert all CSV files in directory and subdirectories to JSON
python main.py --convert-to csv --path output/json # Convert all JSON files in directory and subdirectories to CSV
python main.py --convert-to json --year 2023       # Convert only 2023 CSV files to JSON
```

## Directory Structure
For the new implementation, we'll maintain two parallel directory structures for CSV and JSON:

```
output/
├── csv/
│   ├── 2023/
│   │   �� qb_stats.csv
│   │   ├── rb_stats.csv
│   │   ├── te_stats.csv
│   │   └── wr_stats.csv
│   └── 2022/
│       ├── qb_stats.csv
│       ├── rb_stats.csv
│       ├── te_stats.csv
│       └── wr_stats.csv
└── json/
    ├── 2023/
    │   ├── qb_stats.json
    │   ├── rb_stats.json
    │   ├── te_stats.json
    │   └── wr_stats.json
    └── 2022/
        ├── qb_stats.json
        ├── rb_stats.json
        ├── te_stats.json
        └── wr_stats.json
```

When converting from the old structure to the new format:
```
output/                    →    output/
├── 2023/                       ├── csv/2023/
│   ├── qb_stats.csv           │   ├── qb_stats.csv
│   ├── rb_stats.csv           │   ├── rb_stats.csv
│   ├── te_stats.csv           │   ├── te_stats.csv
│   └── wr_stats.csv           │   └── wr_stats.csv
                               └── json/2023/
                                   ├── qb_stats.json
                                   ├── rb_stats.json
                                   ├── te_stats.json
                                   └── wr_stats.json
```

## Implementation Details

### 1. Argument Parsing
- Add argument parsing using Python's `argparse` module
- Define mutually exclusive groups for:
  - --csv and --json flags (for scraping)
  - --convert-to option with 'json' or 'csv' value
- Make --csv the default option if no format is specified
- Add optional arguments:
  - --year for specific year conversion
  - --path for directory-wide conversion

### 2. Code Changes Required
1. Modify the main script to:
   - Add argument parsing for output format and conversion operations
   - Create new functions for JSON conversion
   - Implement logic to choose between scraping and conversion modes

2. Create new conversion functions:
   ```python
   def convert_to_json(data, output_file):
       # Convert DataFrame to JSON
       # Save to specified output file

   def convert_directory(source_path, target_format, year=None):
       # Convert all files in the source directory and subdirectories to the target format
       # If year is specified, only convert files in that year's subdirectory
       # Maintain same file structure in output directory
       # Return summary of converted files

   def get_target_path(source_path, source_format, target_format):
       # Generate the target path by replacing format directory
       # Example: output/csv/2023/qb_stats.csv -> output/json/2023/qb_stats.json
       # Handle old format: output/2023/qb_stats.csv -> output/json/2023/qb_stats.json
   ```

3. Update the existing code structure:
   - Keep CSV as default format for scraping
   - Add conditional logic to determine operation mode (scrape vs convert)
   - Maintain consistent file naming convention across formats
   - Implement proper error handling for missing directories/files
   - Add progress tracking for bulk conversions

### 3. Output Format
The JSON output will maintain exactly the same structure as the CSV files, with each player's data represented as a JSON object. The keys in the JSON objects will exactly match the CSV headers.

Example for QB stats:
```json
[
    {
        "Rank": "1",
        "Player": "Peyton Manning",
        "Team": "DEN",
        "G": "16",
        "COMP": "450",
        "ATT": "659",
        "PCT": "68",
        "YDS": "5477",
        "Y/A": "8.3",
        "AIR": "3062",
        "AIR/A": "4.6",
        "10+ YDS": "223",
        "20+ YDS": "68",
        "30+ YDS": "33",
        "40+ YDS": "13",
        "50+ YDS": "8",
        "PKT TIME": "0.0",
        "SACK": "18",
        "KNCK": "0",
        "HRRY": "0",
        "BLITZ": "160",
        "POOR": "0",
        "DROP": "43",
        "RZ ATT": "110",
        "RTG": "114"
    }
]
```

Example for RB stats:
```json
[
    {
        "Rank": "1",
        "Player": "Jamaal Charles",
        "Team": "KC",
        "G": "15",
        "ATT": "259",
        "YDS": "1287",
        "Y/ATT": "5.0",
        "YBCON": "709",
        "YBCON/ATT": "2.7",
        "YACON (Rushing)": "578",
        "YACON/ATT": "2.2",
        "BRKTKL": "0",
        "TK LOSS": "12",
        "TK LOSS YDS": "-23",
        "LNG TD": "31",
        "10+ YDS": "37",
        "20+ YDS": "6",
        "30+ YDS": "5",
        "40+ YDS": "1",
        "50+ YDS": "0",
        "LNG": "46",
        "REC": "70",
        "TGT": "104",
        "RZ TGT": "17",
        "YACON (Receiving)": "0"
    }
]
```

## Testing Plan
1. Test command-line argument parsing
2. Verify JSON output format and structure
3. Ensure CSV functionality remains unchanged
4. Test conversion operations:
   - CSV to JSON conversion
   - JSON to CSV conversion
   - Directory structure preservation
   - Recursive directory conversion
   - Year-specific conversion
   - Old format to new format conversion
5. Test edge cases:
   - Invalid arguments
   - Missing data handling
   - Large dataset handling
   - Missing source directories/files
   - Partial conversions (some files missing)
   - Mixed format directories
   - Deep directory structures
   - Converting from old directory structure

## Future Considerations
1. Potential for additional output formats
2. Option to specify custom output file names
3. Possibility of concurrent format outputs
4. Batch conversion of multiple years
5. Validation of converted data integrity
6. Progress bar for bulk conversions
7. Conversion summary report
8. Migration utility for old directory structure

## Roadmap

The following features and improvements are organized into phases based on priority and dependencies:

### Phase 1: Core Functionality & Data Integrity
Essential features needed for reliable operation:

1. Data Type Handling
   - Preserve data types when converting between formats
   - Proper handling of numeric fields (store as numbers in JSON)
   - Basic handling of null values and empty strings

2. Basic Error Handling & Validation
   - JSON schema validation
   - Basic error reporting
   - Data integrity checks during conversion

3. Critical CLI Options
   ```bash
   --force       # Overwrite existing files without prompting
   --backup      # Create backups before conversion
   ```

4. Essential Testing
   - Data integrity testing
   - Round-trip conversion testing
   - Basic error handling tests

### Phase 2: Safety & Reliability
Features to ensure safe and reliable operation:

1. Enhanced Error Handling
   - Detailed error reporting and logging
   - Malformed JSON handling
   - Validation of numeric ranges and data formats

2. Migration Safety Features
   - Rollback mechanism for failed conversions
   - Source/target comparison
   - Automatic backups

3. Extended CLI Options
   ```bash
   --dry-run     # Preview conversion operations
   --verbose     # Enable detailed logging
   --quiet       # Suppress all non-error output
   ```

4. Basic Security Features
   - Input validation and sanitization
   - Safe file path handling
   - Basic permissions checking

### Phase 3: Performance & Scalability
Optimizations for handling larger datasets:

1. Performance Optimizations
   - Streaming support for large files
   - Memory optimization for bulk operations
   - Basic parallel processing

2. Advanced Output Options
   - Pretty print vs. minified JSON
   - Basic formatting controls
   - Custom indentation levels

3. Extended Testing
   - Performance testing
   - Memory usage testing
   - Large file handling tests

### Phase 4: Advanced Features
Nice-to-have features for better user experience:

1. Advanced CLI Features
   ```bash
   --log-file    # Specify custom log file location
   ```

2. Format Options
   - JSONL (JSON Lines) format support
   - CSV formatting options (delimiters, quotes)
   - Advanced JSON formatting controls

3. Documentation
   - Comprehensive error message guide
   - Troubleshooting documentation
   - API documentation

### Phase 5: Enterprise Features
Features for production/enterprise use:

1. Advanced Performance
   - Advanced parallel processing
   - Caching mechanisms
   - Batch processing optimizations

2. Monitoring & Reporting
   - Conversion statistics
   - Error rate tracking
   - Performance metrics
   - Automated report generation

3. Advanced Security
   - Audit logging
   - Advanced permissions management
   - Secure backup storage

4. Advanced Testing
   - Concurrent access testing
   - Race condition prevention
   - Advanced performance benchmarking

Each phase builds upon the previous ones, with each new phase adding more sophisticated features while maintaining stability. Implementation will proceed phase by phase, with user feedback potentially adjusting priorities within and between phases.