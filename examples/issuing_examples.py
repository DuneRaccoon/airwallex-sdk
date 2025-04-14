"""
Airwallex SDK Issuing API Usage Examples
"""
import asyncio
import os
from datetime import datetime, timedelta

from airwallex import (
    AirwallexClient, 
    AirwallexAsyncClient,
    IssuingCardholderModel,
    IssuingCardModel
)
from airwallex.models.issuing_cardholder import CardholderCreateRequest, Individual, Name, Address
from airwallex.models.issuing_card import CardCreateRequest, AuthorizationControls, CardProgram
from airwallex.models.issuing_transaction_dispute import TransactionDisputeCreateRequest


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
        # Get issuing configuration
        print("==== Getting Issuing Configuration ====")
        config = client.issuing_config.get_config()
        print(f"Remote auth enabled: {config.remote_auth_settings.enabled if config.remote_auth_settings else 'Not configured'}")
        
        # Create a cardholder
        print("\n==== Creating a Cardholder ====")
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
        
        try:
            cardholder = client.issuing_cardholder.create_cardholder(cardholder_request)
            print(f"Cardholder created with ID: {cardholder.cardholder_id}")
            
            # List cardholders
            print("\n==== Listing Cardholders ====")
            cardholders = client.issuing_cardholder.list_with_filters(page_size=5)
            for ch in cardholders:
                print(f"Cardholder: {ch.cardholder_id} - {ch.email} - Status: {ch.status}")
            
            # Create a card for the cardholder
            print("\n==== Creating a Card ====")
            card_request = CardCreateRequest(
                cardholder_id=cardholder.cardholder_id,
                request_id="test-request-" + datetime.now().strftime("%Y%m%d%H%M%S"),
                created_by="API Test User",
                form_factor="VIRTUAL",
                is_personalized=True,
                authorization_controls=AuthorizationControls(
                    allowed_currencies=["USD", "AUD"],
                    allowed_transaction_count="MULTIPLE"
                ),
                program=CardProgram(
                    id="default_program_id",  # This would need to be replaced with a real program ID
                    name="Default Program"
                )
            )
            
            try:
                card = client.issuing_card.create_card(card_request)
                print(f"Card created with ID: {card.card_id}")
                
                # Get card details
                print("\n==== Getting Card Details ====")
                try:
                    card_details = client.issuing_card.get_card_details(card.card_id)
                    print(f"Card Number: {card_details.card_number}")
                    print(f"CVV: {card_details.cvv}")
                    print(f"Expiry: {card_details.expiry_month}/{card_details.expiry_year}")
                except Exception as e:
                    print(f"Could not retrieve card details: {str(e)}")
                
                # List cards
                print("\n==== Listing Cards ====")
                cards = client.issuing_card.list_with_filters(page_size=5)
                for c in cards:
                    print(f"Card: {c.card_id} - Status: {c.card_status}")
                
                # List transactions
                print("\n==== Listing Transactions ====")
                transactions = client.issuing_transaction.list_with_filters(
                    card_id=card.card_id,
                    page_size=5
                )
                if transactions:
                    for tx in transactions:
                        print(f"Transaction: {tx.transaction_id} - {tx.transaction_amount} {tx.transaction_currency}")
                else:
                    print("No transactions found for this card.")
                
                # Create a transaction dispute (example)
                print("\n==== Creating a Transaction Dispute (Example) ====")
                if transactions:
                    dispute_request = TransactionDisputeCreateRequest(
                        transaction_id=transactions[0].transaction_id,
                        reason="SUSPECTED_FRAUD",
                        notes="This is a test dispute"
                    )
                    
                    try:
                        dispute = client.issuing_transaction_dispute.create_dispute(dispute_request)
                        print(f"Dispute created with ID: {dispute.id}")
                    except Exception as e:
                        print(f"Could not create dispute: {str(e)}")
                else:
                    print("No transactions available to dispute.")
                
            except Exception as e:
                print(f"Card creation failed: {str(e)}")
                
        except Exception as e:
            print(f"Cardholder creation failed: {str(e)}")
            
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
        # Get issuing configuration
        print("==== Async: Getting Issuing Configuration ====")
        config = await client.issuing_config.get_config_async()
        print(f"Remote auth enabled: {config.remote_auth_settings.enabled if config.remote_auth_settings else 'Not configured'}")
        
        # List cardholders
        print("\n==== Async: Listing Cardholders ====")
        cardholders = await client.issuing_cardholder.list_with_filters_async(page_size=5)
        for ch in cardholders:
            print(f"Cardholder: {ch.cardholder_id} - {ch.email} - Status: {ch.status}")
        
        # List cards
        print("\n==== Async: Listing Cards ====")
        cards = await client.issuing_card.list_with_filters_async(page_size=5)
        for c in cards:
            print(f"Card: {c.card_id} - Status: {c.card_status}")
        
        # List transactions
        print("\n==== Async: Listing Transactions ====")
        transactions = await client.issuing_transaction.list_with_filters_async(page_size=5)
        for tx in transactions:
            print(f"Transaction: {tx.transaction_id} - {tx.transaction_amount} {tx.transaction_currency}")
        
        # Use pagination generator
        print("\n==== Async: Using Pagination Generator for Cards ====")
        count = 0
        async for card in client.issuing_card.paginate_async_generator(page_size=2):
            print(f"Card {count}: {card.card_id}")
            count += 1
            if count >= 5:
                break
                
    finally:
        # Close the client
        await client.close()


if __name__ == "__main__":
    print("Running synchronous examples...")
    try:
        sync_examples()
    except Exception as e:
        print(f"Synchronous examples failed: {str(e)}")
    
    print("\n\nRunning asynchronous examples...")
    try:
        asyncio.run(async_examples())
    except Exception as e:
        print(f"Asynchronous examples failed: {str(e)}")
