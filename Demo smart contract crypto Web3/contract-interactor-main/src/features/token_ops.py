# src/features/token_ops.py
from pathlib import Path
import json
from typing import Any, Dict, Optional, Tuple

from web3 import Web3
from web3.types import HexBytes, TxReceipt

try:
    from web3.contract.contract import Contract
except ImportError:
    from web3.contract import Contract  # type: ignore[attr-defined]

from src.core.logger import get_logger
from src.core.web3_provider import get_web3
from src.blockchain.contract_loader import load_contract
from src.blockchain.transaction_manager import send_contract_transaction

logger = get_logger(__name__)

ERC20_ABI_PATH = Path("abis/ltc_token.json.json")


def _load_erc20_abi() -> list[dict[str, Any]]:

    if not ERC20_ABI_PATH.is_file():
        raise FileNotFoundError(
            f"ERC-20 ABI file not found at {ERC20_ABI_PATH}. "
            "Create it and put the minimal ERC-20 ABI JSON array inside."
        )

    try:
        raw = ERC20_ABI_PATH.read_text(encoding="utf-8")
        abi = json.loads(raw)
    except Exception as e:
        raise RuntimeError(f"Failed to read ERC-20 ABI from {ERC20_ABI_PATH}: {e}")

    if not isinstance(abi, list):
        raise ValueError(
            f"ERC-20 ABI file {ERC20_ABI_PATH} must contain a JSON list, got {type(abi)}"
        )

    return abi  # type: ignore[return-value]


def load_token_contract(
    token_address: str,
    web3: Web3 | None = None,
) -> Contract:

    if web3 is None:
        web3 = get_web3()

    abi = _load_erc20_abi()
    contract = load_contract(address=token_address, abi=abi, web3=web3)
    return contract


def get_token_metadata(
    token_address: str,
    web3: Web3 | None = None,
) -> Dict[str, Any]:

    contract = load_token_contract(token_address, web3)

    try:
        name = contract.functions.name().call()
    except Exception:
        name = None

    try:
        symbol = contract.functions.symbol().call()
    except Exception:
        symbol = None

    try:
        decimals = contract.functions.decimals().call()
    except Exception:
        decimals = None

    meta = {
        "address": token_address,
        "name": name,
        "symbol": symbol,
        "decimals": decimals,
    }

    logger.info(f"Token metadata: {meta}")
    return meta


def get_token_balance(
    token_address: str,
    owner_address: str,
    web3: Web3 | None = None,
) -> int:

    if web3 is None:
        web3 = get_web3()

    contract = load_token_contract(token_address, web3)

    balance = contract.functions.balanceOf(owner_address).call()
    logger.info(
        f"Token balance for {owner_address} on token {token_address}: {balance}"
    )
    return int(balance)


def transfer_token(
    token_address: str,
    to_address: str,
    amount_raw: int,
    web3: Web3 | None = None,
    wait: bool = True,
    timeout: int = 120,
    poll_latency: int = 2,
) -> Tuple[HexBytes, Optional[TxReceipt]]:

    if web3 is None:
        web3 = get_web3()

    contract = load_token_contract(token_address, web3)

    fn = contract.functions.transfer(to_address, amount_raw)

    logger.info(
        f"Transferring {amount_raw} units of token {token_address} to {to_address}"
    )

    tx_hash, receipt = send_contract_transaction(
        fn,
        value_wei=0,
        wait=wait,
        timeout=timeout,
        poll_latency=poll_latency,
    )

    return tx_hash, receipt
