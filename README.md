# UNOFFICIAL Airwallex Python SDK

A fully-featured SDK for interacting with the [Airwallex API](https://www.airwallex.com/docs/api).

## Features

- Comprehensive implementation of the Airwallex API
- Both synchronous and asynchronous client support
- Automatic authentication and token refresh
- Built-in rate limiting and retry logic
- Type checking with Pydantic models
- Pagination handling

## Installation

```bash
pip install airwallex-sdk
```

## Quick Start

### Synchronous Usage

```python
from airwallex import AirwallexClient
from airwallex.models.payment import PaymentCreateRequest, PaymentAmount

# Initialize the client
client = AirwallexClient(
    client_id="your_client_id",
    api_key="your_api_key"
)

# List accounts
accounts = client.accounts.list()
for account in accounts:
    print(f"Account: {account.account_name} ({account.id})")

# Fetch a specific account
account = client.accounts.fetch("account_id")
print(account.show())  # Print a formatted representation

# Create a payment
payment_request = PaymentCreateRequest(
    request_id="unique_request_id",
    amount=PaymentAmount(value=100.00, currency="USD"),
    source={
        "type": "account",
        "account_id": "account_id"
    },
    beneficiary={
        "type": "bank_account",
        "id": "beneficiary_id"
    },
    payment_method="swift"
)

payment = client.payments.create_from_model(payment_request)
print(f"Payment created with ID: {payment.id}")

# Use generator to iterate through all payments
for payment in client.payments():
    print(f"Payment {payment.id}: {payment.amount.value} {payment.amount.currency}")
```

### Asynchronous Usage

```python
import asyncio
from airwallex import AirwallexAsyncClient
from airwallex.models.beneficiary import BeneficiaryCreateRequest, BankDetails

async def main():
    # Initialize the async client
    client = AirwallexAsyncClient(
        client_id="your_client_id",
        api_key="your_api_key"
    )
    
    # List accounts
    accounts = await client.accounts.list_async()
    
    # Create a beneficiary
    beneficiary_request = BeneficiaryCreateRequest(
        name="John Doe",
        type="bank_account",
        bank_details=BankDetails(
            account_name="John Doe",
            account_number="123456789",
            swift_code="ABCDEFGH",
            bank_country_code="US"
        )
    )
    
    beneficiary = await client.beneficiaries.create_from_model_async(beneficiary_request)
    print(f"Beneficiary created with ID: {beneficiary.id}")
    
    # Async generator to iterate through all beneficiaries
    async for ben in client.beneficiaries.paginate_async_generator():
        print(f"Beneficiary: {ben.name}")
    
    await client.close()

# Run the async function
asyncio.run(main())
```

## Documentation

For detailed documentation, see [https://www.airwallex.com/docs/api](https://www.airwallex.com/docs/api).

## License

This project is licensed under the MIT License - see the LICENSE file for details.
