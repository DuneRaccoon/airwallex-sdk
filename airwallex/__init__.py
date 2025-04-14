"""
Airwallex Python SDK.

A fully-featured SDK for interacting with the Airwallex API.
"""
from .client import AirwallexClient, AirwallexAsyncClient
from .exceptions import (
    AirwallexAPIError,
    AuthenticationError,
    RateLimitError,
    ResourceNotFoundError,
    ValidationError,
    ServerError
)

# Import models
from .models import AirwallexModel
from .models.account import Account as AccountModel
from .models.payment import Payment as PaymentModel
from .models.beneficiary import Beneficiary as BeneficiaryModel
from .models.invoice import Invoice as InvoiceModel, InvoiceItem
from .models.financial_transaction import FinancialTransaction as FinancialTransactionModel

__all__ = [
    "AirwallexClient",
    "AirwallexAsyncClient",
    "AirwallexAPIError",
    "AuthenticationError",
    "RateLimitError",
    "ResourceNotFoundError",
    "ValidationError",
    "ServerError",
    "AirwallexModel",
    "AccountModel",
    "PaymentModel",
    "BeneficiaryModel",
    "InvoiceModel",
    "InvoiceItem",
    "FinancialTransactionModel",
]

__version__ = "0.1.0"