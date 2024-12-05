#!/bin/bash

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Loop through years 2013-2023
for year in {2013..2023}; do
    echo "Processing year $year..."
    python main.py $year
    
    # Check if the script executed successfully
    if [ $? -ne 0 ]; then
        echo "Error processing year $year"
        exit 1
    fi
    
    echo "Completed processing for year $year"
    echo "----------------------------------------"
done

echo "All years processed successfully!" 