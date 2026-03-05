from typing import Any, Optional, Tuple

from web3 import Web3
from web3.types import HexBytes, TxReceipt

try:
    # Web3.py v6 location
    from web3.contract.contract import Contract
except ImportError:
    # Fallback for older versions
    from web3.contract import Contract  # type: ignore[attr-defined]

from src.core.logger import get_logger
from src.core.web3_provider import get_web3
from src.core.exceptions import ContractLoadError
from src.blockchain.contract_loader import load_contract, list_contract_methods
from src.blockchain.transaction_manager import send_contract_transaction

logger = get_logger(__name__)


# --------- Core helpers using an already-loaded Contract ---------


def call_read_only_method(
    contract: Contract,
    method_name: str,
    *args: Any,
) -> Any:

    logger.info(f"Calling read-only method '{method_name}' with args={args}")

    try:
        fn = getattr(contract.functions, method_name)(*args)
    except AttributeError:
        raise ContractLoadError(f"Method '{method_name}' not found on contract")

    try:
        result = fn.call()
    except Exception as e:
        logger.error(f"Error calling read-only method '{method_name}': {e}")
        raise

    logger.debug(f"Result of '{method_name}': {result}")
    return result


def send_write_method_tx(
    contract: Contract,
    method_name: str,
    *args: Any,
    value_wei: int = 0,
    wait: bool = True,
    timeout: int = 120,
    poll_latency: int = 2,
) -> Tuple[HexBytes, Optional[TxReceipt]]:

    logger.info(
        f"Sending write tx to method '{method_name}' with args={args}, "
        f"value_wei={value_wei}"
    )

    try:
        fn = getattr(contract.functions, method_name)(*args)
    except AttributeError:
        raise ContractLoadError(f"Method '{method_name}' not found on contract")

    tx_hash, receipt = send_contract_transaction(
        fn,
        value_wei=value_wei,
        wait=wait,
        timeout=timeout,
        poll_latency=poll_latency,
    )

    return tx_hash, receipt


# --------- Convenience helpers: address + ABI in one shot ---------


def load_contract_and_inspect(
    address: str,
    abi: Any,
    web3: Web3 | None = None,
) -> tuple[Contract, dict]:
    contract = load_contract(address=address, abi=abi, web3=web3)
    methods_info = list_contract_methods(contract)
    return contract, methods_info


def call_read_only_with_address(
    address: str,
    abi: Any,
    method_name: str,
    *args: Any,
    web3: Web3 | None = None,
) -> Any:
    """
    Convenience wrapper:
      1) load contract from address + ABI
      2) call a read-only method
    """
    if web3 is None:
        web3 = get_web3()

    contract = load_contract(address=address, abi=abi, web3=web3)
    return call_read_only_method(contract, method_name, *args)


def send_write_tx_with_address(
    address: str,
    abi: Any,
    method_name: str,
    *args: Any,
    value_wei: int = 0,
    wait: bool = True,
    timeout: int = 120,
    poll_latency: int = 2,
    web3: Web3 | None = None,
) -> Tuple[HexBytes, Optional[TxReceipt]]:
    """
    Convenience wrapper:
      1) load contract from address + ABI
      2) send tx to write method
    """
    if web3 is None:
        web3 = get_web3()

    contract = load_contract(address=address, abi=abi, web3=web3)
    return send_write_method_tx(
        contract=contract,
        method_name=method_name,
        *args,
        value_wei=value_wei,
        wait=wait,
        timeout=timeout,
        poll_latency=poll_latency,
    )
