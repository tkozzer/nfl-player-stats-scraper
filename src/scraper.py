"""
NFL Player Stats Scraper - Web Scraping Module
"""
import time
from typing import Dict, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup

class NFLStatsScraper:
    """
    A class to scrape NFL player statistics from FantasyPros.com
    """
    
    BASE_URL = "https://www.fantasypros.com/nfl/advanced-stats-{position}.php"
    MIN_YEAR = 2013
    MAX_YEAR = 2024
    VALID_POSITIONS = ['qb', 'rb', 'wr', 'te']
    
    def __init__(self):
        self.session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,  # number of retries
            backoff_factor=0.5,  # wait 0.5, 1, 2... seconds between retries
            status_forcelist=[500, 502, 503, 504]  # HTTP status codes to retry on
        )
        
        # Mount the adapter with retry strategy for both http and https
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Add headers to mimic browser behavior
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        })
    
    def validate_year(self, year: int) -> bool:
        """Validate that the year is within acceptable range."""
        return self.MIN_YEAR <= year <= self.MAX_YEAR
    
    def validate_position(self, position: str) -> bool:
        """Validate that the position is supported."""
        return position.lower() in self.VALID_POSITIONS
    
    def get_url(self, position: str, year: int) -> str:
        """Generate the URL for the given position and year."""
        return f"{self.BASE_URL.format(position=position)}?year={year}"
    
    def fetch_stats(self, position: str, year: int, max_retries: int = 3) -> Optional[str]:
        """
        Fetch stats for a given position and year.
        
        Args:
            position: NFL position (qb, rb, wr, te)
            year: Season year
            max_retries: Maximum number of retry attempts
            
        Returns:
            HTML content of the stats page or None if failed
        """
        if not self.validate_year(year):
            raise ValueError(f"Year must be between {self.MIN_YEAR} and {self.MAX_YEAR}")
        
        if not self.validate_position(position):
            raise ValueError(f"Position must be one of {self.VALID_POSITIONS}")
        
        url = self.get_url(position, year)
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # Increased timeout to 30 seconds
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                # Add delay between requests to be respectful
                time.sleep(2)  # Increased delay to 2 seconds
                
                return response.text
                
            except requests.RequestException as e:
                print(f"Error fetching data (attempt {retry_count + 1}/{max_retries}): {str(e)}")
                retry_count += 1
                if retry_count < max_retries:
                    wait_time = 2 ** retry_count + 1  # Modified exponential backoff
                    print(f"Waiting {wait_time} seconds before retrying...")
                    time.sleep(wait_time)
        
        return None
    
    def extract_table_data(self, html_content: str) -> Dict:
        """
        Extract table headers and data from HTML content.
        
        Args:
            html_content: Raw HTML content
            
        Returns:
            Dictionary containing headers and data
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table', {'id': 'data'})
        
        if not table:
            raise ValueError("Could not find stats table in HTML content")
        
        # Extract headers from the second row (first row contains category groupings)
        headers = ['Rank', 'Player', 'Team']  # Start with Rank, Player, and Team
        header_rows = table.find('thead').find_all('tr')
        if len(header_rows) >= 2:  # Make sure we have at least 2 rows
            header_row = header_rows[1]  # Get the second row
            for th in header_row.find_all('th')[2:]:  # Skip rank and player columns
                # For all other columns, use the text inside the small tag as the abbreviation
                small_tag = th.find('small')
                if small_tag:
                    # Get the text content and clean it up
                    header_text = small_tag.text.strip()
                    # Some abbreviations have newlines and extra spaces, clean those up
                    header_text = ' '.join(header_text.split())
                    headers.append(header_text)
                else:
                    # Fallback to th text if no small tag
                    headers.append(th.text.strip())
        
        # Extract data rows
        data = []
        body = table.find('tbody')
        if body:
            for row in body.find_all('tr'):
                row_data = []
                cells = row.find_all('td')
                
                # Add rank
                row_data.append(cells[0].text.strip())
                
                # Handle player cell and team
                player_cell = cells[1]
                if 'player-label' in player_cell.get('class', []):
                    # Extract player name
                    player_name = player_cell.find('a')
                    if player_name:
                        row_data.append(player_name.text.strip())
                    else:
                        row_data.append('')
                    
                    # Extract team name
                    team = player_cell.find('small')
                    if team:
                        # Remove parentheses from team name
                        team_name = team.text.strip().strip('()')
                        row_data.append(team_name)
                    else:
                        row_data.append('')
                else:
                    row_data.extend(['', ''])  # Empty player and team if not found
                
                # Handle remaining stats (skip first two cells - rank and player)
                for td in cells[2:]:
                    row_data.append(td.text.strip())
                
                data.append(row_data)
        
        return {
            'headers': headers,
            'data': data
        }

if __name__ == "__main__":
    # Example usage
    scraper = NFLStatsScraper()
    html = scraper.fetch_stats('qb', 2023)
    if html:
        data = scraper.extract_table_data(html)
        print(f"Found {len(data['data'])} players")
        print("data:", data)
        print("Headers:", data['headers']) 