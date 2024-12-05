import csv
import os
from typing import Tuple, List

def validate_csv(file_path: str) -> Tuple[bool, List[str]]:
    """
    Validates a CSV file by checking:
    1. File exists
    2. File is readable
    3. File has consistent number of columns
    4. File has valid CSV formatting
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        Tuple[bool, List[str]]: (is_valid, list of error messages)
    """
    errors = []
    
    # Check if file exists
    if not os.path.exists(file_path):
        return False, ["File does not exist"]
    
    # Check if file is empty
    if os.path.getsize(file_path) == 0:
        return False, ["File is empty"]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            
            # Get header
            header = next(reader, None)
            if not header:
                return False, ["CSV file has no header row"]
            
            expected_columns = len(header)
            
            # Check for duplicate headers
            if len(header) != len(set(header)):
                errors.append("CSV contains duplicate column headers")
            
            # Validate each row
            for row_num, row in enumerate(reader, start=2):
                if len(row) != expected_columns:
                    errors.append(f"Row {row_num} has {len(row)} columns, expected {expected_columns}")
                
                # Check for empty values
                for col_num, value in enumerate(row):
                    if not value.strip():
                        errors.append(f"Empty value found in row {row_num}, column {col_num + 1}")
                        
    except csv.Error as e:
        return False, [f"CSV parsing error: {str(e)}"]
    except Exception as e:
        return False, [f"Unexpected error: {str(e)}"]
    
    if errors:
        return False, errors
    
    return True, []

def main():
    """
    Main function to demonstrate CSV validation
    """
    # Example usage
    csv_file = "player_stats.csv"  # Update this with your CSV file path
    is_valid, errors = validate_csv(csv_file)
    
    if is_valid:
        print(f"✅ {csv_file} is a valid CSV file")
    else:
        print(f"❌ {csv_file} validation failed:")
        for error in errors:
            print(f"  - {error}")

if __name__ == "__main__":
    main() 