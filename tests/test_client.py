"""
Tests for the Airwallex SDK client.
"""
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import json

from airwallex import AirwallexClient, AirwallexAsyncClient
from airwallex.exceptions import AuthenticationError, create_exception_from_response


class TestAirwallexClient(unittest.TestCase):
    """Tests for the AirwallexClient class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client_id = "test_client_id"
        self.api_key = "test_api_key"
        
    @patch('httpx.Client.post')
    def test_authentication(self, mock_post):
        """Test authentication flow."""
        # Mock response for authentication
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "token": "test_token",
            "expires_at": (datetime.now() + timedelta(minutes=30)).isoformat()
        }
        mock_post.return_value = mock_response
        
        # Initialize client and authenticate
        client = AirwallexClient(client_id=self.client_id, api_key=self.api_key)
        client.authenticate()
        
        # Check authentication request
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['headers']['x-client-id'], self.client_id)
        self.assertEqual(kwargs['headers']['x-api-key'], self.api_key)
        
        # Check token is stored
        self.assertEqual(client._token, "test_token")
        self.assertIsNotNone(client._token_expiry)
    
    @patch('httpx.Client.post')
    def test_authentication_error(self, mock_post):
        """Test authentication error handling."""
        # Mock authentication error
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "code": "credentials_invalid",
            "message": "Invalid credentials"
        }
        mock_post.return_value = mock_response
        
        # Initialize client
        client = AirwallexClient(client_id=self.client_id, api_key=self.api_key)
        
        # Authentication should raise error
        with self.assertRaises(AuthenticationError):
            client.authenticate()
    
    @patch('httpx.Client.request')
    @patch('httpx.Client.post')
    def test_request_with_authentication(self, mock_post, mock_request):
        """Test request flow with authentication."""
        # Mock authentication response
        auth_response = MagicMock()
        auth_response.status_code = 201
        auth_response.json.return_value = {
            "token": "test_token",
            "expires_at": (datetime.now() + timedelta(minutes=30)).isoformat()
        }
        mock_post.return_value = auth_response
        
        # Mock API request response
        request_response = MagicMock()
        request_response.status_code = 200
        request_response.json.return_value = {"id": "test_id", "name": "Test Account"}
        mock_request.return_value = request_response
        
        # Initialize client
        client = AirwallexClient(client_id=self.client_id, api_key=self.api_key)
        
        # Make request
        response = client._request("GET", "/api/v1/test")
        
        # Check authentication was called
        mock_post.assert_called_once()
        
        # Check request was made with authentication token
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(args[0], "GET")
        self.assertEqual(args[1], "/api/v1/test")
        self.assertEqual(kwargs['headers']['Authorization'], "Bearer test_token")
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": "test_id", "name": "Test Account"})


if __name__ == '__main__':
    unittest.main()
