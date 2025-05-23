# UNOFFICIAL Airwallex Python SDK

A simple SDK for interacting with the [Airwallex API](https://www.airwallex.com/docs/api).

## Features

- SOMEWHAT Comprehensive implementation of the Airwallex API
- Both synchronous and asynchronous client support
- Automatic authentication and token refresh
- Built-in rate limiting and retry logic
- Type checking with Pydantic models

## Installation

```bash
pip install airwallex-sdk
```

## Quick Start

### Payments API

#### Synchronous Usage

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

#### Asynchronous Usage

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

### Issuing API

#### Working with Cardholders and Cards

```python
from airwallex import AirwallexClient
from airwallex.models.issuing_cardholder import CardholderCreateRequest, Individual, Name, Address
from airwallex.models.issuing_card import CardCreateRequest, AuthorizationControls, CardProgram

# Initialize the client
client = AirwallexClient(
    client_id="your_client_id",
    api_key="your_api_key"
)

# Create a cardholder
cardholder_request = CardholderCreateRequest(
    email="john.doe@example.com",
    individual=Individual(
        name=Name(
            first_name="John",
            last_name="Doe",
            title="Mr"
        ),
        date_of_birth="1982-11-02",
        address=Address(
            city="Melbourne",
            country="AU",
            line1="44 Example St",
            postcode="3121",
            state="VIC"
        ),
        cardholder_agreement_terms_consent_obtained="yes",
        express_consent_obtained="yes"
    ),
    type="INDIVIDUAL"
)

cardholder = client.issuing_cardholder.create_cardholder(cardholder_request)
print(f"Cardholder created with ID: {cardholder.cardholder_id}")

# Create a virtual card
card_request = CardCreateRequest(
    cardholder_id=cardholder.cardholder_id,
    request_id="unique-request-id",
    created_by="API User",
    form_factor="VIRTUAL",
    is_personalized=True,
    authorization_controls=AuthorizationControls(
        allowed_currencies=["USD", "AUD"],
        allowed_transaction_count="MULTIPLE"
    ),
    program=CardProgram(
        id="your_program_id",
        name="Default Program"
    )
)

card = client.issuing_card.create_card(card_request)
print(f"Card created with ID: {card.card_id}")

# Get card details
card_details = client.issuing_card.get_card_details(card.card_id)
print(f"Card Number: {card_details.card_number}")
print(f"CVV: {card_details.cvv}")
print(f"Expiry: {card_details.expiry_month}/{card_details.expiry_year}")
```

## Documentation

For detailed documentation, see [https://www.airwallex.com/docs/api](https://www.airwallex.com/docs/api).

## License

This project is licensed under the MIT License - see the LICENSE file for details.
