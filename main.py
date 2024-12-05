import sys
from src.writer import scrape_and_save_all
from src.validate import validate_csv
from pathlib import Path

def main():
    """
    Main function to scrape NFL stats, save to CSV, and validate the files.
    """
    # Get year from command line or use default
    if len(sys.argv) > 1:
        year = int(sys.argv[1])
    else:
        year = 2023

    print(f"\nProcessing NFL stats for {year}...")
    
    # Scrape and save data for all positions
    results = scrape_and_save_all(year)
    
    # Validate each CSV file
    all_valid = True
    
    print("\nValidating CSV files...")
    for position, filepath in results.items():
        is_valid, errors = validate_csv(filepath)
        
        if is_valid:
            print(f"✅ {position.upper()}: {Path(filepath).name} is valid")
        else:
            all_valid = False
            print(f"❌ {position.upper()}: {Path(filepath).name} has errors:")
            for error in errors:
                print(f"  - {error}")
    
    # Final status
    print("\nFinal Status:")
    if all_valid:
        print("✅ All CSV files are valid")
        sys.exit(0)
    else:
        print("❌ Some CSV files have validation errors")
        sys.exit(1)

if __name__ == "__main__":
    main() 