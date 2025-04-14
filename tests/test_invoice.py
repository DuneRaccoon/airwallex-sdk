"""
Tests for the Airwallex SDK invoice API.
"""
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from airwallex import AirwallexClient
from airwallex.models.invoice import (
    Invoice, 
    InvoiceItem, 
    InvoicePreviewRequest, 
    InvoicePreviewResponse
)


class TestInvoiceAPI(unittest.TestCase):
    """Tests for the Invoice API."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client_id = "test_client_id"
        self.api_key = "test_api_key"
        
        # Create a client with authentication mocked
        patcher = patch.object(AirwallexClient, 'authenticate')
        self.mock_auth = patcher.start()
        self.addCleanup(patcher.stop)
        
        self.client = AirwallexClient(client_id=self.client_id, api_key=self.api_key)
        self.client._token = "test_token"
        self.client._token_expiry = datetime.now() + timedelta(minutes=30)
    
    @patch('httpx.Client.request')
    def test_list_invoices(self, mock_request):
        """Test listing invoices."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "id": "inv_test123",
                    "customer_id": "cus_test456",
                    "currency": "USD",
                    "total_amount": 100.00,
                    "status": "PAID",
                    "period_start_at": "2023-01-01T00:00:00Z",
                    "period_end_at": "2023-02-01T00:00:00Z",
                    "created_at": "2023-01-01T00:00:00Z"
                }
            ],
            "has_more": False
        }
        mock_request.return_value = mock_response
        
        # Call list method
        invoices = self.client.invoice.list()
        
        # Check request was made correctly
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(args[0], "GET")
        self.assertTrue(args[1].endswith("/invoices"))
        
        # Check response parsing
        self.assertEqual(len(invoices), 1)
        self.assertIsInstance(invoices[0], Invoice)
        self.assertEqual(invoices[0].id, "inv_test123")
        self.assertEqual(invoices[0].currency, "USD")
        self.assertEqual(invoices[0].total_amount, 100.00)
    
    @patch('httpx.Client.request')
    def test_get_invoice(self, mock_request):
        """Test fetching a single invoice."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "inv_test123",
            "customer_id": "cus_test456",
            "currency": "USD",
            "total_amount": 100.00,
            "status": "PAID",
            "period_start_at": "2023-01-01T00:00:00Z",
            "period_end_at": "2023-02-01T00:00:00Z",
            "created_at": "2023-01-01T00:00:00Z"
        }
        mock_request.return_value = mock_response
        
        # Call fetch method
        invoice = self.client.invoice.fetch("inv_test123")
        
        # Check request was made correctly
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(args[0], "GET")
        self.assertTrue(args[1].endswith("/invoices/inv_test123"))
        
        # Check response parsing
        self.assertIsInstance(invoice, Invoice)
        self.assertEqual(invoice.id, "inv_test123")
        self.assertEqual(invoice.currency, "USD")
        self.assertEqual(invoice.total_amount, 100.00)
    
    @patch('httpx.Client.request')
    def test_preview_invoice(self, mock_request):
        """Test previewing an invoice."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "customer_id": "cus_test456",
            "currency": "USD",
            "total_amount": 100.00,
            "created_at": "2023-01-01T00:00:00Z",
            "items": [
                {
                    "id": "item_test123",
                    "invoice_id": "inv_test123",
                    "amount": 100.00,
                    "currency": "USD",
                    "period_start_at": "2023-01-01T00:00:00Z",
                    "period_end_at": "2023-02-01T00:00:00Z",
                    "price": {
                        "id": "pri_test123",
                        "name": "Test Price",
                        "active": True,
                        "currency": "USD",
                        "product_id": "prod_test123",
                        "pricing_model": "flat"
                    }
                }
            ]
        }
        mock_request.return_value = mock_response
        
        # Create preview request
        preview_request = InvoicePreviewRequest(
            customer_id="cus_test456",
            items=[
                InvoicePreviewRequest.SubscriptionItem(
                    price_id="pri_test123",
                    quantity=1
                )
            ]
        )
        
        # Call preview method
        preview = self.client.invoice.preview(preview_request)
        
        # Check request was made correctly
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertTrue(args[1].endswith("/invoices/preview"))
        
        # Check response parsing
        self.assertIsInstance(preview, InvoicePreviewResponse)
        self.assertEqual(preview.customer_id, "cus_test456")
        self.assertEqual(preview.currency, "USD")
        self.assertEqual(preview.total_amount, 100.00)
        self.assertEqual(len(preview.items), 1)
        self.assertEqual(preview.items[0].amount, 100.00)


if __name__ == '__main__':
    unittest.main()
