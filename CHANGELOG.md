# Changelog

All notable changes to the Airwallex SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-04-14

### Added

- Support for the Issuing API, including:
  - Authorizations management
  - Cardholders management
  - Cards management
  - Digital wallet tokens management
  - Transaction disputes management
  - Transactions management
  - Issuing configuration
- Improved pagination handling with support for `has_more` responses
- Additional examples for Issuing API usage

## [0.1.0] - 2025-04-14

### Added

- Initial release of the Airwallex Python SDK
- Support for both synchronous and asynchronous API requests
- Automatic authentication and token refresh
- Comprehensive type checking with Pydantic models
- Support for the following API endpoints:
  - Account management
  - Balance operations
  - Payment processing
  - Beneficiary management 
  - FX operations
  - Invoice management
- Pagination support for listing operations
- Error handling with detailed exception types
- Comprehensive documentation
