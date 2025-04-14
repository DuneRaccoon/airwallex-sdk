"""
Tests for the Airwallex SDK exception handling.
"""
import unittest
from unittest.mock import MagicMock
import json

from airwallex.exceptions import (
    AirwallexAPIError,
    AuthenticationError,
    RateLimitError,
    ResourceNotFoundError,
    ValidationError,
    ServerError,
    ResourceExistsError,
    AmountLimitError,
    EditForbiddenError,
    CurrencyError,
    DateError,
    TransferMethodError,
    ConversionError,
    ServiceUnavailableError,
    create_exception_from_response
)


class TestExceptions(unittest.TestCase):
    """Tests for the exception handling system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_response = MagicMock()
        self.method = "GET"
        self.url = "/api/v1/test"
        self.kwargs = {"headers": {"Authorization": "Bearer test_token"}}
    
    def test_exception_from_status_code(self):
        """Test creating exceptions based only on status code."""
        # 401 should create AuthenticationError
        self.mock_response.status_code = 401
        self.mock_response.json.side_effect = ValueError("Invalid JSON")
        
        exception = create_exception_from_response(
            response=self.mock_response,
            method=self.method,
            url=self.url,
            kwargs=self.kwargs
        )
        
        self.assertIsInstance(exception, AuthenticationError)
        self.assertEqual(exception.status_code, 401)
        
        # 404 should create ResourceNotFoundError
        self.mock_response.status_code = 404
        
        exception = create_exception_from_response(
            response=self.mock_response,
            method=self.method,
            url=self.url,
            kwargs=self.kwargs
        )
        
        self.assertIsInstance(exception, ResourceNotFoundError)
        self.assertEqual(exception.status_code, 404)
        
        # 429 should create RateLimitError
        self.mock_response.status_code = 429
        
        exception = create_exception_from_response(
            response=self.mock_response,
            method=self.method,
            url=self.url,
            kwargs=self.kwargs
        )
        
        self.assertIsInstance(exception, RateLimitError)
        self.assertEqual(exception.status_code, 429)
        
        # 400 should create ValidationError
        self.mock_response.status_code = 400
        
        exception = create_exception_from_response(
            response=self.mock_response,
            method=self.method,
            url=self.url,
            kwargs=self.kwargs
        )
        
        self.assertIsInstance(exception, ValidationError)
        self.assertEqual(exception.status_code, 400)
        
        # 500 should create ServerError
        self.mock_response.status_code = 500
        
        exception = create_exception_from_response(
            response=self.mock_response,
            method=self.method,
            url=self.url,
            kwargs=self.kwargs
        )
        
        self.assertIsInstance(exception, ServerError)
        self.assertEqual(exception.status_code, 500)
    
    def test_exception_from_error_code(self):
        """Test creating exceptions based on error code."""
        self.mock_response.status_code = 400
        
        # Test credentials_invalid (should be AuthenticationError)
        self.mock_response.json.return_value = {
            "code": "credentials_invalid",
            "message": "Invalid credentials",
            "source": "api_key"
        }
        
        exception = create_exception_from_response(
            response=self.mock_response,
            method=self.method,
            url=self.url,
            kwargs=self.kwargs
        )
        
        self.assertIsInstance(exception, AuthenticationError)
        self.assertEqual(exception.error_code, "credentials_invalid")
        self.assertEqual(exception.error_source, "api_key")
        
        # Test already_exists (should be ResourceExistsError)
        self.mock_response.json.return_value = {
            "code": "already_exists",
            "message": "Resource already exists",
            "source": "id"
        }
        
        exception = create_exception_from_response(
            response=self.mock_response,
            method=self.method,
            url=self.url,
            kwargs=self.kwargs
        )
        
        self.assertIsInstance(exception, ResourceExistsError)
        self.assertEqual(exception.error_code, "already_exists")
        
        # Test amount_above_limit (should be AmountLimitError)
        self.mock_response.json.return_value = {
            "code": "amount_above_limit",
            "message": "Amount exceeds the maximum limit",
            "source": "amount"
        }
        
        exception = create_exception_from_response(
            response=self.mock_response,
            method=self.method,
            url=self.url,
            kwargs=self.kwargs
        )
        
        self.assertIsInstance(exception, AmountLimitError)
        self.assertEqual(exception.error_code, "amount_above_limit")
        
        # Test invalid_currency_pair (should be CurrencyError)
        self.mock_response.json.return_value = {
            "code": "invalid_currency_pair",
            "message": "The currency pair is invalid",
            "source": "currency_pair"
        }
        
        exception = create_exception_from_response(
            response=self.mock_response,
            method=self.method,
            url=self.url,
            kwargs=self.kwargs
        )
        
        self.assertIsInstance(exception, CurrencyError)
        self.assertEqual(exception.error_code, "invalid_currency_pair")
        
        # Test invalid_transfer_date (should be DateError)
        self.mock_response.json.return_value = {
            "code": "invalid_transfer_date",
            "message": "The transfer date is invalid",
            "source": "transfer_date"
        }
        
        exception = create_exception_from_response(
            response=self.mock_response,
            method=self.method,
            url=self.url,
            kwargs=self.kwargs
        )
        
        self.assertIsInstance(exception, DateError)
        self.assertEqual(exception.error_code, "invalid_transfer_date")
        
        # Test service_unavailable (should be ServiceUnavailableError)
        self.mock_response.status_code = 503
        self.mock_response.json.return_value = {
            "code": "service_unavailable",
            "message": "The service is currently unavailable",
        }
        
        exception = create_exception_from_response(
            response=self.mock_response,
            method=self.method,
            url=self.url,
            kwargs=self.kwargs
        )
        
        self.assertIsInstance(exception, ServiceUnavailableError)
        self.assertEqual(exception.error_code, "service_unavailable")
    
    def test_exception_string_representation(self):
        """Test the string representation of exceptions."""
        self.mock_response.status_code = 400
        self.mock_response.json.return_value = {
            "code": "invalid_argument",
            "message": "The argument is invalid",
            "source": "amount"
        }
        
        exception = create_exception_from_response(
            response=self.mock_response,
            method=self.method,
            url=self.url,
            kwargs=self.kwargs
        )
        
        expected_str = "Airwallex API Error (HTTP 400): [invalid_argument] The argument is invalid (source: amount) for GET /api/v1/test"
        self.assertEqual(str(exception), expected_str)
        
        # Test without source
        self.mock_response.json.return_value = {
            "code": "invalid_argument",
            "message": "The argument is invalid"
        }
        
        exception = create_exception_from_response(
            response=self.mock_response,
            method=self.method,
            url=self.url,
            kwargs=self.kwargs
        )
        
        expected_str = "Airwallex API Error (HTTP 400): [invalid_argument] The argument is invalid for GET /api/v1/test"
        self.assertEqual(str(exception), expected_str)


if __name__ == '__main__':
    unittest.main()
