#!/bin/bash

# Function to display usage
show_usage() {
    echo "Usage: $0 [--format FORMAT]"
    echo "FORMAT options: csv (default), json"
    exit 1
}

# Default format
FORMAT="csv"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --format)
            if [[ $2 != "csv" && $2 != "json" ]]; then
                echo "Error: Format must be either 'csv' or 'json'"
                show_usage
            fi
            FORMAT=$2
            shift 2
            ;;
        *)
            echo "Error: Unknown argument $1"
            show_usage
            ;;
    esac
done

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

echo "Starting batch processing in $FORMAT format..."

# Loop through years 2013-2023
for year in {2013..2023}; do
    echo "Processing year $year..."
    if [ "$FORMAT" = "json" ]; then
        python main.py $year --json
    else
        python main.py $year --csv
    fi
    
    # Check if the script executed successfully
    if [ $? -ne 0 ]; then
        echo "Error processing year $year"
        exit 1
    fi
    
    echo "Completed processing for year $year"
    echo "----------------------------------------"
done

echo "All years processed successfully in $FORMAT format!" 