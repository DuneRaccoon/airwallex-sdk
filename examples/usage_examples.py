"""
Airwallex SDK Usage Examples
"""
import asyncio
import os
from datetime import datetime, timedelta

from airwallex import (
    AirwallexClient, 
    AirwallexAsyncClient,
    InvoiceModel
)
from airwallex.models.invoice import InvoicePreviewRequest


def get_client_credentials():
    """Get client credentials from environment variables."""
    client_id = os.environ.get("AIRWALLEX_CLIENT_ID")
    api_key = os.environ.get("AIRWALLEX_API_KEY")
    
    if not client_id or not api_key:
        raise ValueError(
            "Please set AIRWALLEX_CLIENT_ID and AIRWALLEX_API_KEY environment variables"
        )
        
    return client_id, api_key


def sync_examples():
    """Examples using the synchronous client."""
    client_id, api_key = get_client_credentials()
    
    # Initialize the client
    client = AirwallexClient(
        client_id=client_id,
        api_key=api_key
    )
    
    try:
        # List accounts
        print("==== Listing Accounts ====")
        accounts = client.account.list()
        for account in accounts:
            print(f"Account: {account.id} - {account.account_currency}")
            
        # Get account details
        if accounts:
            print(f"\n==== Account Details for {accounts[0].id} ====")
            account = client.account.fetch(accounts[0].id)
            print(account.show())
            
        # List invoices
        print("\n==== Listing Invoices ====")
        invoices = client.invoice.list()
        for invoice in invoices:
            print(f"Invoice: {invoice.id} - {invoice.total_amount} {invoice.currency}")
            
        # List invoice with filtering
        print("\n==== Filtered Invoices (last 30 days) ====")
        thirty_days_ago = datetime.now() - timedelta(days=30)
        filtered_invoices = client.invoice.list_with_filters(
            from_created_at=thirty_days_ago,
            status="PAID"
        )
        for invoice in filtered_invoices:
            print(f"Invoice: {invoice.id} - Status: {invoice.status}")
            
        # If we have an invoice, get its items
        if invoices:
            invoice_id = invoices[0].id
            print(f"\n==== Items for Invoice {invoice_id} ====")
            items = client.invoice.list_items(invoice_id)
            for item in items:
                print(f"Item: {item.id} - {item.amount} {item.currency}")
                
        # Preview an invoice (example)
        print("\n==== Invoice Preview Example ====")
        preview_request = InvoicePreviewRequest(
            customer_id="cus_example123",
            items=[
                InvoicePreviewRequest.SubscriptionItem(
                    price_id="pri_example456",
                    quantity=2
                )
            ],
            recurring={
                "period": 1,
                "period_unit": "MONTH"
            }
        )
        
        try:
            # Note: this will likely fail without valid IDs
            preview = client.invoice.preview(preview_request)
            print(f"Preview: {preview.total_amount} {preview.currency}")
        except Exception as e:
            print(f"Preview failed (expected without valid IDs): {str(e)}")
            
    finally:
        # Close the client
        client.close()


async def async_examples():
    """Examples using the asynchronous client."""
    client_id, api_key = get_client_credentials()
    
    # Initialize the async client
    client = AirwallexAsyncClient(
        client_id=client_id,
        api_key=api_key
    )
    
    try:
        # List accounts
        print("==== Async: Listing Accounts ====")
        accounts = await client.account.list_async()
        for account in accounts:
            print(f"Account: {account.id} - {account.account_currency}")
            
        # List invoices
        print("\n==== Async: Listing Invoices ====")
        invoices = await client.invoice.list_async()
        for invoice in invoices:
            print(f"Invoice: {invoice.id} - {invoice.total_amount} {invoice.currency}")
            
        # Use pagination generator
        print("\n==== Async: Iterating Through Invoices ====")
        count = 0
        async for invoice in client.invoice.paginate_async_generator(page_size=5):
            print(f"Invoice {count}: {invoice.id}")
            count += 1
            if count >= 10:
                break
                
    finally:
        # Close the client
        await client.close()


if __name__ == "__main__":
    print("Running synchronous examples...")
    sync_examples()
    
    print("\n\nRunning asynchronous examples...")
    asyncio.run(async_examples())
