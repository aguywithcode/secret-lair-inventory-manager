import os
import json
import pytest
import responses
from bs4 import BeautifulSoup
from unittest.mock import patch, MagicMock, mock_open, ANY

# Add project root to path for imports
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.scrape_secret_lairs import (
    parse_card_number_range,
    find_matching_cards,
    scrape_secret_lairs,
    save_to_json
)

class TestScrapeSL:
    """Tests for the scrape_secret_lairs module"""
    
    def test_parse_card_number_range_simple(self):
        """Test parsing a simple card number range"""
        result = parse_card_number_range("SLD-123 - SLD-129")
        assert result['type'] == 'list'
        assert result['set'] == 'SLD'
        assert result['numbers'] == [123, 124, 125, 126, 127, 128, 129]
    
    def test_parse_card_number_range_list(self):
        """Test parsing a comma-separated list of card numbers"""
        result = parse_card_number_range("SLD-123, SLD-125, SLD-127")
        assert result['type'] == 'list'
        assert result['set'] == 'SLD'
        assert result['numbers'] == [123, 125, 127]
    
    def test_parse_card_number_range_mixed(self):
        """Test parsing a mixed format with ranges and individual numbers"""
        result = parse_card_number_range("SLD-123 - SLD-125, SLD-130")
        assert result['type'] == 'list'
        assert result['set'] == 'SLD'
        assert result['numbers'] == [123, 124, 125, 130]
    
    def test_parse_card_number_simple_numbers(self):
        """Test parsing simple numbers without set code"""
        result = parse_card_number_range("123 - 125")
        assert result['type'] == 'list'
        assert result['set'] == 'SLD'  # Default set code
        assert result['numbers'] == [123, 124, 125]
    
    def test_parse_card_number_invalid(self):
        """Test parsing an invalid format"""
        result = parse_card_number_range("Invalid Format")
        assert result is None
    
    def test_find_matching_cards(self):
        """Test finding matching cards from Scryfall data"""
        # Sample Scryfall data
        scryfall_data = [
            {
                "name": "Test Card 1",
                "set": "sld",
                "collector_number": "123",
                "prices": {"usd": "10.99", "usd_foil": "20.99"},
                "image_uris": {"normal": "https://example.com/image1.jpg"}
            },
            {
                "name": "Test Card 2",
                "set": "sld",
                "collector_number": "124",
                "prices": {"usd": "5.99", "usd_foil": "15.99"},
                "image_uris": {"normal": "https://example.com/image2.jpg"}
            },
            {
                "name": "Non-SLD Card",
                "set": "eld",
                "collector_number": "123",
                "prices": {"usd": "1.99", "usd_foil": "3.99"},
                "image_uris": {"normal": "https://example.com/image3.jpg"}
            }
        ]
        
        # Card range to look for
        card_range = {
            'type': 'list',
            'set': 'SLD',
            'numbers': [123, 124]
        }
        
        # Find matching cards
        result = find_matching_cards(scryfall_data, card_range)
        
        assert len(result) == 2
        assert result[0]["name"] == "Test Card 1"
        assert result[1]["name"] == "Test Card 2"
    
    def test_find_matching_cards_no_matches(self):
        """Test finding matching cards with no matches"""
        # Sample Scryfall data
        scryfall_data = [
            {
                "name": "Non-matching Card",
                "set": "sld",
                "collector_number": "500",
                "prices": {"usd": "10.99", "usd_foil": "20.99"}
            }
        ]
        
        # Card range to look for
        card_range = {
            'type': 'list',
            'set': 'SLD',
            'numbers': [123, 124]
        }
        
        # Find matching cards (should be empty)
        result = find_matching_cards(scryfall_data, card_range)
        assert len(result) == 0
    
    @responses.activate
    @patch('scripts.scrape_secret_lairs.load_scryfall_data')
    def test_scrape_secret_lairs(self, mock_load_scryfall):
        """Test scraping Secret Lair data from MTG Wiki"""
        # Create mock HTML response
        html_content = """
        <html>
        <body>
            <table class="wikitable">
                <tr>
                    <th>Drop #</th>
                    <th>Name</th>
                    <th>Cards</th>
                </tr>
                <tr>
                    <td>123</td>
                    <td>Test Secret Lair</td>
                    <td>SLD-123 - SLD-125</td>
                </tr>
                <tr>
                    <td>124</td>
                    <td>Another Secret Lair</td>
                    <td>SLD-130, SLD-131</td>
                </tr>
            </table>
        </body>
        </html>
        """
        
        # Mock the HTTP response
        responses.add(
            responses.GET,
            "https://mtg.wiki/page/Secret_Lair/Drop_Series",
            body=html_content,
            status=200
        )
        
        # Mock Scryfall data (not matching with Scryfall)
        mock_load_scryfall.return_value = None
        
        # Call the function
        result = scrape_secret_lairs()
        
        # Check the result
        assert len(result) == 2
        assert result[0]["drop_number"] == "123"
        assert result[0]["name"] == "Test Secret Lair"
        assert result[0]["card_numbers"] == "SLD-123 - SLD-125"
        assert result[1]["drop_number"] == "124"
        assert result[1]["name"] == "Another Secret Lair"
        assert result[1]["card_numbers"] == "SLD-130, SLD-131"
    
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_to_json(self, mock_file_open, mock_makedirs):
        """Test saving data to JSON file"""
        # Test data
        test_data = [
            {"name": "Test Drop", "cards": ["Card 1", "Card 2"]}
        ]
        
        # Call the function
        save_to_json(test_data, filename="test.json", directory="test_dir")
        
        # Check that the directory was created
        mock_makedirs.assert_called_once_with("test_dir", exist_ok=True)
        
        # Check that the file was opened correctly
        mock_file_open.assert_called_once_with(
            os.path.join("test_dir", "test.json"),
            'w',
            encoding='utf-8'
        )
        
        # Instead of checking the number of write calls, verify that json.dump was called
        # with the correct data by checking what was passed to the file handle
        handle = mock_file_open()
        # The data argument should be our test_data, ANY is used for the file handle and other arguments
        with patch('json.dump') as mock_json_dump:
            save_to_json(test_data, filename="test.json", directory="test_dir")
            mock_json_dump.assert_called_once_with(test_data, ANY, indent=2, ensure_ascii=False)