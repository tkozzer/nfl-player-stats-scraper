import pytest
from src.scraper import NFLStatsScraper
from unittest.mock import patch, MagicMock
import requests

@pytest.fixture
def scraper():
    return NFLStatsScraper()

@pytest.fixture
def sample_html():
    return """
    <table id="data">
        <thead>
            <tr class="header-row">
                <th>Category 1</th>
                <th>Category 2</th>
            </tr>
            <tr>
                <th>Rank</th>
                <th>Player<br/><small>Team</small></th>
                <th>Stats<br/><small>YDS</small></th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td class="player-label">
                    <a>Tom Brady</a>
                    <small>(TB)</small>
                </td>
                <td>4000</td>
            </tr>
        </tbody>
    </table>
    """

def test_scraper_initialization(scraper):
    """Test that scraper initializes with correct default values."""
    assert isinstance(scraper, NFLStatsScraper)
    assert scraper.BASE_URL == "https://www.fantasypros.com/nfl/advanced-stats-{position}.php"
    assert scraper.MIN_YEAR == 2013
    assert scraper.MAX_YEAR == 2024
    assert scraper.VALID_POSITIONS == ['qb', 'rb', 'wr', 'te']

def test_validate_year(scraper):
    """Test year validation."""
    # Valid years
    assert scraper.validate_year(2023) is True
    assert scraper.validate_year(2013) is True
    assert scraper.validate_year(2024) is True
    
    # Invalid years
    assert scraper.validate_year(2012) is False
    assert scraper.validate_year(2025) is False

def test_validate_position(scraper):
    """Test position validation."""
    # Valid positions
    assert scraper.validate_position('qb') is True
    assert scraper.validate_position('QB') is True
    assert scraper.validate_position('rb') is True
    
    # Invalid positions
    assert scraper.validate_position('kicker') is False
    assert scraper.validate_position('') is False

def test_get_url(scraper):
    """Test URL generation."""
    url = scraper.get_url('qb', 2023)
    assert 'qb' in url.lower()
    assert '2023' in url
    assert url.startswith('https://')

@patch('src.scraper.requests.Session.get')
def test_fetch_stats_success(mock_get, scraper):
    """Test successful stats fetching."""
    # Mock successful response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "<html>Success</html>"
    mock_get.return_value = mock_response

    result = scraper.fetch_stats("qb", 2023)
    assert result == "<html>Success</html>"
    mock_get.assert_called_once()

@patch('src.scraper.requests.Session.get')
def test_fetch_stats_failure(mock_get, scraper):
    """Test failed stats fetching."""
    # Mock failed response
    mock_get.side_effect = requests.RequestException("Connection error")

    result = scraper.fetch_stats("qb", 2023)
    assert result is None
    assert mock_get.call_count > 0  # Should have attempted retries

def test_fetch_stats_invalid_inputs(scraper):
    """Test fetch_stats with invalid inputs."""
    with pytest.raises(ValueError):
        scraper.fetch_stats("invalid", 2023)
    
    with pytest.raises(ValueError):
        scraper.fetch_stats("qb", 2000)

def test_extract_table_data(scraper, sample_html):
    """Test extraction of table data from HTML."""
    data = scraper.extract_table_data(sample_html)
    
    # Check structure
    assert 'headers' in data
    assert 'data' in data
    
    # Check headers
    assert 'Rank' in data['headers']
    assert 'Player' in data['headers']
    
    # Check data
    assert len(data['data']) == 1
    assert 'Tom Brady' in data['data'][0]
    assert 'TB' in data['data'][0]

def test_extract_table_data_no_table(scraper):
    """Test table extraction with invalid HTML."""
    with pytest.raises(ValueError):
        scraper.extract_table_data("<html>No table here</html>") 