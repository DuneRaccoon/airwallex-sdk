from airwallex import AirwallexClient, AirwallexAsyncClient

# Synchronous example
client = AirwallexClient(client_id="your_client_id", api_key="your_api_key")

# Fetch a specific financial transaction
transaction = client.financial_transaction.fetch("transaction_id")
print(f"Transaction: {transaction.id} - {transaction.amount} {transaction.currency}")

# List financial transactions with filters
from datetime import datetime, timedelta
thirty_days_ago = datetime.now() - timedelta(days=30)

transactions = client.financial_transaction.list_with_filters(
    from_created_at=thirty_days_ago,
    status="SETTLED"
)

for tx in transactions:
    print(f"Transaction: {tx.id} - {tx.amount} {tx.currency}")

async def main_async():
# Asynchronous example
    async with AirwallexAsyncClient(client_id="your_client_id", api_key="your_api_key") as client:
        # List transactions using async pagination
        async for tx in client.financial_transaction.paginate_async_generator():
            print(f"Transaction: {tx.id} - {tx.amount} {tx.currency}")