# src/core/exceptions.py

class NetworkError(Exception):
    """Problems connecting to the blockchain network."""

class ContractLoadError(Exception):
    """Problems loading or working with a smart contract."""

class TransactionError(Exception):
    """Problems while building / signing / sending transactions."""
