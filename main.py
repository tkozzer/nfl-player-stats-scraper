import sys
import argparse
from pathlib import Path
from src.writer import scrape_and_save_all
from src.validate import validate_csv
from src.converter import NFLStatsConverter

def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description='NFL Player Stats Scraper')
    
    # Create mutually exclusive group for format options
    format_group = parser.add_mutually_exclusive_group()
    format_group.add_argument('--json', action='store_true', help='Save output in JSON format')
    format_group.add_argument('--csv', action='store_true', help='Save output in CSV format (default)')
    
    # Create mutually exclusive group for operation mode
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('year', nargs='?', type=int, help='Year to scrape data for (default: 2023)')
    mode_group.add_argument('--convert-to', choices=['json', 'csv'], help='Convert existing files to specified format')
    
    # Optional arguments for conversion
    parser.add_argument('--path', type=str, help='Directory path for conversion')
    
    args = parser.parse_args()
    
    # Set default year if not provided
    if not args.convert_to and not args.year:
        args.year = 2023
    
    return args

def handle_conversion(target_format: str, path: str = None, year: int = None):
    """
    Handle file format conversion.
    
    Args:
        target_format: Target format ('csv' or 'json')
        path: Optional directory path to convert
        year: Optional year to convert
    """
    converter = NFLStatsConverter()
    
    print(f"\nConverting files to {target_format.upper()}...")
    if path:
        print(f"Source directory: {path}")
    if year:
        print(f"Year: {year}")
    
    results = converter.convert_files(target_format, path, year)
    
    # Print results
    if results['success']:
        print("\nSuccessfully converted files:")
        for message in results['success']:
            print(f"✅ {message}")
    
    if results['errors']:
        print("\nErrors during conversion:")
        for message in results['errors']:
            print(f"❌ {message}")
    
    # Return appropriate exit code
    return 0 if not results['errors'] else 1

def main():
    """
    Main function to scrape NFL stats and save to specified format.
    """
    args = parse_args()
    
    # Handle conversion mode
    if args.convert_to:
        sys.exit(handle_conversion(args.convert_to, args.path, args.year))
    
    # Handle scraping mode
    output_format = 'json' if args.json else 'csv'
    print(f"\nProcessing NFL stats for {args.year}...")
    
    # Scrape and save data for all positions
    results = scrape_and_save_all(args.year, output_format=output_format)
    
    # Validate each file
    all_valid = True
    
    if output_format == 'csv':
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
    else:
        print("\nJSON validation will be implemented in a future update.")
    
    # Final status
    print("\nFinal Status:")
    if output_format == 'csv':
        if all_valid:
            print("✅ All CSV files are valid")
            sys.exit(0)
        else:
            print("❌ Some CSV files have validation errors")
            sys.exit(1)
    else:
        print("✅ All JSON files have been created")
        sys.exit(0)

if __name__ == "__main__":
    main() 