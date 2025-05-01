import os
import json
import pytest
from unittest.mock import patch, mock_open

# Add project root to path for imports
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.app import app

@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestWebApp:
    """Tests for the Flask web application"""
    
    @patch('web.app.load_secret_lairs')
    def test_index_route(self, mock_load_secret_lairs, client):
        """Test the index route"""
        # Mock the secret lairs data
        mock_secret_lairs = [
            {
                "drop_number": "123",
                "name": "Test Secret Lair",
                "card_numbers": "SLD-123 - SLD-125",
                "cards": [
                    {
                        "name": "Test Card 1",
                        "collector_number": "123",
                        "set": "sld",
                        "prices": {"usd": "10.99", "usd_foil": "20.99"},
                        "image_uri": "https://example.com/image1.jpg"
                    }
                ]
            }
        ]
        mock_load_secret_lairs.return_value = mock_secret_lairs
        
        # Make a request to the index route
        response = client.get('/')
        
        # Check the response
        assert response.status_code == 200
        assert b'Secret Lair Drops' in response.data
        assert b'Test Secret Lair' in response.data
    
    @patch('web.app.load_secret_lairs')
    def test_detail_route(self, mock_load_secret_lairs, client):
        """Test the secret lair detail route"""
        # Mock the secret lairs data
        mock_secret_lairs = [
            {
                "drop_number": "123",
                "name": "Test Secret Lair",
                "card_numbers": "SLD-123 - SLD-125",
                "cards": [
                    {
                        "name": "Test Card 1",
                        "collector_number": "123",
                        "set": "sld",
                        "prices": {"usd": "10.99", "usd_foil": "20.99"},
                        "image_uri": "https://example.com/image1.jpg"
                    }
                ]
            }
        ]
        mock_load_secret_lairs.return_value = mock_secret_lairs
        
        # Make a request to the detail route
        response = client.get('/secret-lair/123')
        
        # Check the response
        assert response.status_code == 200
        assert b'Test Secret Lair' in response.data
        assert b'Test Card 1' in response.data
    
    @patch('web.app.load_secret_lairs')
    def test_detail_route_not_found(self, mock_load_secret_lairs, client):
        """Test the detail route with a non-existent drop number"""
        # Mock the secret lairs data
        mock_load_secret_lairs.return_value = []
        
        # Make a request to a non-existent detail route
        response = client.get('/secret-lair/999')
        
        # Check that we get a 404 response
        assert response.status_code == 404
    
    @patch('web.app.load_secret_lairs')
    def test_api_secret_lairs(self, mock_load_secret_lairs, client):
        """Test the API endpoint for all secret lairs"""
        # Mock the secret lairs data
        mock_secret_lairs = [
            {
                "drop_number": "123",
                "name": "Test Secret Lair"
            }
        ]
        mock_load_secret_lairs.return_value = mock_secret_lairs
        
        # Make a request to the API route
        response = client.get('/api/secret-lairs')
        
        # Check the response
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]["drop_number"] == "123"
        assert data[0]["name"] == "Test Secret Lair"
    
    @patch('web.app.load_secret_lairs')
    def test_api_secret_lair_detail(self, mock_load_secret_lairs, client):
        """Test the API endpoint for a specific secret lair"""
        # Mock the secret lairs data
        mock_secret_lairs = [
            {
                "drop_number": "123",
                "name": "Test Secret Lair",
                "cards": [{"name": "Test Card"}]
            }
        ]
        mock_load_secret_lairs.return_value = mock_secret_lairs
        
        # Make a request to the API detail route
        response = client.get('/api/secret-lair/123')
        
        # Check the response
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["drop_number"] == "123"
        assert data["name"] == "Test Secret Lair"
        assert len(data["cards"]) == 1
    
    @patch('web.app.load_secret_lairs')
    def test_api_secret_lair_detail_not_found(self, mock_load_secret_lairs, client):
        """Test the API detail route with a non-existent drop number"""
        # Mock the secret lairs data
        mock_load_secret_lairs.return_value = []
        
        # Make a request to a non-existent API detail route
        response = client.get('/api/secret-lair/999')
        
        # Check that we get a 404 response
        assert response.status_code == 404
    
    def test_page_not_found(self, client):
        """Test the 404 error handler"""
        # Make a request to a non-existent route
        response = client.get('/non-existent-route')
        
        # Check that we get a 404 response with our custom page
        assert response.status_code == 404
        assert b'Page Not Found' in response.data

    def test_format_price_utility(self):
        """Test the format_price utility function"""
        # Import the function directly from the app
        from web.app import utility_processor
        
        # Get the utility functions
        utils = utility_processor()
        format_price = utils['format_price']
        
        # Test various price formats
        assert format_price("10.99") == "$10.99"
        assert format_price(5) == "$5.00"
        assert format_price(None) == "N/A"
        assert format_price("invalid") == "N/A"