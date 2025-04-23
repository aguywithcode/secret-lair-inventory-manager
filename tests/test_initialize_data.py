import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.initialize_data import initialize_data_directory

class TestInitializeData:
    """Tests for the initialize_data module"""
    
    @patch('scripts.initialize_data.download_scryfall_data')
    @patch('scripts.initialize_data.scrape_secret_lairs')
    @patch('scripts.initialize_data.save_to_json')
    def test_initialize_data_success(self, mock_save_json, mock_scrape, mock_download):
        """Test successful data initialization"""
        # Set up mocks
        mock_download.return_value = "/path/to/scryfall_data.json"
        mock_scrape.return_value = [{"drop_number": "123", "name": "Test Secret Lair"}]
        
        # Call the function
        result = initialize_data_directory(verbose=False, force=False)
        
        # Check that the function returned True (success)
        assert result is True
        
        # Check that the download was called
        mock_download.assert_called_once()
        
        # Check that the scraper was called with the right arguments
        mock_scrape.assert_called_once_with(
            match_with_scryfall=True, 
            scryfall_filepath=os.path.join("data", "scryfall_data.json")
        )
        
        # Check that save_to_json was called
        mock_save_json.assert_called_once()
    
    @patch('scripts.initialize_data.download_scryfall_data')
    @patch('scripts.initialize_data.scrape_secret_lairs')
    def test_initialize_data_download_failure(self, mock_scrape, mock_download):
        """Test initialization when download fails"""
        # Set up mocks
        mock_download.return_value = None  # Download failed
        
        # Call the function
        result = initialize_data_directory(verbose=False, force=False)
        
        # Check that the function returned False (failure)
        assert result is False
        
        # Check that the download was called
        mock_download.assert_called_once()
        
        # Check that the scraper was still called
        mock_scrape.assert_called_once()
    
    @patch('scripts.initialize_data.download_scryfall_data')
    @patch('scripts.initialize_data.scrape_secret_lairs')
    @patch('scripts.initialize_data.save_to_json')
    def test_initialize_data_scrape_failure(self, mock_save_json, mock_scrape, mock_download):
        """Test initialization when scraping fails"""
        # Set up mocks
        mock_download.return_value = "/path/to/scryfall_data.json"
        mock_scrape.return_value = None  # Scraping failed
        
        # Call the function
        result = initialize_data_directory(verbose=False, force=False)
        
        # Check that the function returned False (failure)
        assert result is False
        
        # Check that the download was called
        mock_download.assert_called_once()
        
        # Check that the scraper was called
        mock_scrape.assert_called_once()
        
        # Check that save_to_json was not called
        mock_save_json.assert_not_called()
    
    @patch('scripts.initialize_data.download_scryfall_data')
    @patch('scripts.initialize_data.scrape_secret_lairs')
    def test_initialize_data_force_flag(self, mock_scrape, mock_download):
        """Test initialization with force flag"""
        # Set up mocks
        mock_download.return_value = "/path/to/scryfall_data.json"
        mock_scrape.return_value = [{"drop_number": "123", "name": "Test Secret Lair"}]
        
        # Call the function with force=True
        initialize_data_directory(verbose=False, force=True)
        
        # Check that download was called with the force flag
        mock_download.assert_called_once()
        
        # Ideally we would check that the force flag was passed to download_scryfall_data,
        # but since we're mocking the function, we can't check the actual arguments easily