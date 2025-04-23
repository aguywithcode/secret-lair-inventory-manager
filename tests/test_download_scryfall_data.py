import os
import json
import pytest
import responses
import tempfile
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Add project root to path for imports
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.download_scryfall_data import (
    get_latest_all_cards_url,
    is_file_recent,
    download_scryfall_data
)

class TestDownloadScryfallData:
    """Tests for the download_scryfall_data module"""
    
    @responses.activate
    def test_get_latest_all_cards_url(self):
        """Test fetching the latest URL for Scryfall bulk data"""
        # Mock the Scryfall API response
        mock_response = {
            "object": "list",
            "data": [
                {
                    "type": "all_cards",
                    "download_uri": "https://scryfall.com/archive/cards/test-data.json",
                    "updated_at": "2025-04-20T12:00:00.000Z",
                    "size": 50000000  # 50MB
                },
                {
                    "type": "default_cards",
                    "download_uri": "https://scryfall.com/archive/cards/default.json",
                    "updated_at": "2025-04-20T12:00:00.000Z",
                    "size": 40000000  # 40MB
                }
            ]
        }
        
        # Setup the mock response
        responses.add(
            responses.GET,
            "https://api.scryfall.com/bulk-data",
            json=mock_response,
            status=200
        )
        
        # Call the function
        url = get_latest_all_cards_url()
        
        # Assert that we got the expected URL
        assert url == "https://scryfall.com/archive/cards/test-data.json"
    
    @responses.activate
    def test_get_latest_all_cards_url_error(self):
        """Test error handling when the API request fails"""
        # Mock an error response
        responses.add(
            responses.GET,
            "https://api.scryfall.com/bulk-data",
            status=500
        )
        
        # Call the function
        url = get_latest_all_cards_url()
        
        # Assert that we got None for the error case
        assert url is None
    
    def test_is_file_recent_nonexistent(self):
        """Test is_file_recent with a nonexistent file"""
        # Test with a file that doesn't exist
        assert is_file_recent('/path/to/nonexistent/file.json') is False
    
    @patch('os.path.exists')
    @patch('os.path.getmtime')
    def test_is_file_recent_recent_file(self, mock_getmtime, mock_exists):
        """Test is_file_recent with a recent file"""
        # Setup mocks
        mock_exists.return_value = True
        
        # Set the file's mtime to 1 hour ago
        current_time = datetime.now().timestamp()
        one_hour_ago = (datetime.now() - timedelta(hours=1)).timestamp()
        mock_getmtime.return_value = one_hour_ago
        
        # File modified 1 hour ago should be considered recent (default is 24 hours)
        assert is_file_recent('test_file.json') is True
    
    @patch('os.path.exists')
    @patch('os.path.getmtime')
    def test_is_file_recent_old_file(self, mock_getmtime, mock_exists):
        """Test is_file_recent with an old file"""
        # Setup mocks
        mock_exists.return_value = True
        
        # Set the file's mtime to 48 hours ago
        two_days_ago = (datetime.now() - timedelta(hours=48)).timestamp()
        mock_getmtime.return_value = two_days_ago
        
        # File modified 48 hours ago should NOT be considered recent (default is 24 hours)
        assert is_file_recent('test_file.json') is False
    
    @responses.activate
    @patch('os.makedirs')
    def test_download_scryfall_data(self, mock_makedirs):
        """Test downloading Scryfall data"""
        # Create a temporary directory and file for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = os.path.join(temp_dir, 'test_data.json')
            
            # Mock the download URL
            test_url = "https://scryfall.com/archive/cards/test-download.json"
            mock_content = json.dumps({"cards": [{"name": "Test Card"}]}).encode('utf-8')
            
            # Setup the mock response
            responses.add(
                responses.GET,
                test_url,
                body=mock_content,
                status=200,
                headers={'content-length': str(len(mock_content))}
            )
            
            # Call the function with our test URL and path
            result = download_scryfall_data(
                url=test_url, 
                directory=temp_dir, 
                filename='test_data.json'
            )
            
            # Check that the file was created
            assert os.path.exists(test_file)
            
            # Verify the content was saved correctly
            with open(test_file, 'rb') as f:
                saved_content = f.read()
            assert saved_content == mock_content
            
            # Check that the function returned the expected path
            assert result == test_file