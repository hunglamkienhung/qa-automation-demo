# BNB Automation Framework (Python + Web3.py)

This project is a Python automation framework for interacting with BNB Smart Chain
(mainnet and testnet) smart contracts.

## Features (planned)

- Connect to BSC mainnet and testnet
- Load contracts via ABI + address
- Inspect contract methods
- Read-only calls
- Write transactions with gas estimation, dynamic gas price, signing, and nonce management
- BEP-20 (ERC-20) token operations
- Scheduling transactions

## Setup

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows

run this command to install lib
pip install -r requirements.txt

run this command to run specific file
 python -m src.cli.get_balance_simple