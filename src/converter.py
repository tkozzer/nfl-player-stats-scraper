"""
NFL Player Stats Converter Module
"""
import os
import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Tuple

class NFLStatsConverter:
    """
    Converter for NFL player statistics between CSV and JSON formats
    """
    
    def __init__(self, base_dir: str = "output"):
        """
        Initialize converter with base output directory.
        
        Args:
            base_dir: Base directory for input/output files
        """
        self.base_dir = Path(base_dir)
    
    def _get_source_files(self, path: str = None, year: int = None) -> List[Path]:
        """
        Get list of files to convert based on path and/or year.
        
        Args:
            path: Optional specific directory path to convert
            year: Optional specific year to convert
            
        Returns:
            List of Path objects for files to convert
        """
        if path:
            source_dir = Path(path)
        else:
            source_dir = self.base_dir
        
        if not source_dir.exists():
            raise FileNotFoundError(f"Source directory {source_dir} does not exist")
        
        # Find all CSV/JSON files recursively
        files = []
        for file_path in source_dir.rglob("*"):
            if not file_path.is_file():
                continue
                
            # Skip files that don't match year if specified
            if year is not None:
                try:
                    file_year = int(file_path.parent.name)
                    if file_year != year:
                        continue
                except ValueError:
                    continue
            
            # Only include CSV/JSON files
            if file_path.suffix.lower() in ['.csv', '.json']:
                files.append(file_path)
        
        return files
    
    def _get_target_path(self, source_path: Path, target_format: str) -> Path:
        """
        Generate target path for converted file.
        
        Args:
            source_path: Source file path
            target_format: Target format ('csv' or 'json')
            
        Returns:
            Path object for target file
        """
        # Determine the year and position from the source path
        try:
            # Try to find year in parent directory name
            year = int(source_path.parent.name)
            # Position is the stem of the filename (e.g., 'qb_stats')
            position = source_path.stem
        except ValueError:
            # If year can't be determined, use the same directory structure
            year = None
            position = source_path.stem
        
        # Create target path
        if year is not None:
            target_dir = self.base_dir / target_format / str(year)
        else:
            # If year unknown, maintain same directory structure but under format dir
            relative_path = source_path.parent.relative_to(self.base_dir)
            target_dir = self.base_dir / target_format / relative_path
        
        target_dir.mkdir(parents=True, exist_ok=True)
        return target_dir / f"{position}.{target_format}"
    
    def convert_file(self, source_path: Path, target_format: str) -> Tuple[bool, str]:
        """
        Convert a single file between CSV and JSON formats.
        
        Args:
            source_path: Path to source file
            target_format: Target format ('csv' or 'json')
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Read source file
            if source_path.suffix.lower() == '.csv':
                df = pd.read_csv(source_path)
            else:  # JSON
                with open(source_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                df = pd.DataFrame(data)
            
            # Get target path
            target_path = self._get_target_path(source_path, target_format)
            
            # Save in target format
            if target_format == 'json':
                json_data = df.to_dict(orient='records')
                with open(target_path, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=4)
            else:  # CSV
                df.to_csv(target_path, index=False)
            
            return True, f"Successfully converted {source_path.name} to {target_path}"
            
        except Exception as e:
            return False, f"Error converting {source_path.name}: {str(e)}"
    
    def convert_files(self, target_format: str, path: str = None, year: int = None) -> Dict[str, List[str]]:
        """
        Convert files between CSV and JSON formats.
        
        Args:
            target_format: Target format ('csv' or 'json')
            path: Optional specific directory path to convert
            year: Optional specific year to convert
            
        Returns:
            Dictionary with 'success' and 'errors' lists of conversion results
        """
        results = {
            'success': [],
            'errors': []
        }
        
        try:
            # Get list of files to convert
            source_files = self._get_source_files(path, year)
            
            if not source_files:
                raise FileNotFoundError("No files found to convert")
            
            # Convert each file
            for source_path in source_files:
                # Skip files already in target format
                if source_path.suffix.lower() == f'.{target_format}':
                    continue
                
                success, message = self.convert_file(source_path, target_format)
                if success:
                    results['success'].append(message)
                else:
                    results['errors'].append(message)
            
            return results
            
        except Exception as e:
            results['errors'].append(f"Error during conversion: {str(e)}")
            return results 