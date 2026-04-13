# src/blockchain/transaction_manager.py

from typing import Optional, Tuple, cast
from web3 import Web3
from web3.types  import HexBytes, TxParams, ChecksumAddress, Wei, Nonce, TxReceipt
from web3.contract.contract  import ContractFunction

# try:
#
#     from web3.contract.contract import ContractFunction
# except ImportError:
#     from web3.contract import ContractFunction


from config.settings import settings
from src.core.logger import get_logger
from src.core.web3_provider import get_web3
from src.core.exceptions import TransactionError
from src.blockchain.account_manager import get_account_manager
from src.blockchain.gas_manager import (
    estimate_gas_for_function,
    get_gas_price,
)

logger = get_logger(__name__)


def build_contract_tx(
    contract_function: ContractFunction,
    value_wei: int = 0,
    gas: Optional[int] = None,
    gas_price: Optional[int] = None,
    nonce: Optional[int] = None,
) -> TxParams:
    web3: Web3 = get_web3()
    account_manager = get_account_manager()

    from_address: ChecksumAddress = web3.to_checksum_address(account_manager.address)

    if nonce is None:
        nonce = account_manager.get_nonce()

    if gas is None:
        gas = estimate_gas_for_function(
            contract_function, from_address=from_address, value_wei=value_wei
        )

    if gas_price is None:
        gas_price = get_gas_price(web3)

    nonce_typed: Nonce = cast(Nonce, nonce)
    gas_price_typed: Wei = cast(Wei, gas_price)
    value_typed: Wei = cast(Wei, value_wei)

    tx_params: TxParams = {
        "from": from_address,
        "nonce": nonce_typed,
        "gas": gas,
        "gasPrice": gas_price_typed,
        "value": value_typed,
        "chainId": settings.chain_id,
    }

    try:
        tx = contract_function.build_transaction(tx_params)
    except Exception as e:
        logger.error(f"Failed to build transaction: {e}")
        raise TransactionError(f"Failed to build transaction: {e}")

    logger.debug(f"Built transaction: {tx}")
    return tx  # type: TxParams




def sign_and_send_transaction(tx: TxParams) -> HexBytes:
    """
    Sign the transaction with the loaded private key and send it.

    Returns:
        tx_hash (HexBytes)
    """
    web3 = get_web3()
    account_manager = get_account_manager()

    try:
        signed = account_manager.sign_transaction(tx)
        tx_hash = web3.eth.send_raw_transaction(signed.raw_transaction)
    except Exception as e:
        logger.error(f"Failed to sign or send transaction: {e}")
        raise TransactionError(f"Failed to sign or send transaction: {e}")

    logger.info(f"Sent transaction: {tx_hash.hex()}")
    return tx_hash


def wait_for_receipt(
    tx_hash: HexBytes,
    timeout: int = 120,
    poll_latency: int = 2,
):

    web3 = get_web3()

    logger.info(f"Waiting for receipt of tx {tx_hash.hex()} ...")
    try:
        receipt = web3.eth.wait_for_transaction_receipt(
            tx_hash,
            timeout=timeout,
            poll_latency=poll_latency,
        )
    except Exception as e:
        logger.error(f"Error while waiting for tx receipt: {e}")
        raise TransactionError(f"Error waiting for tx receipt: {e}")

    logger.info(
        f"Transaction {tx_hash.hex()} mined in block {receipt.get('blockNumber')}, "
        f"status={receipt.get('status')}"
    )
    return receipt


def send_contract_transaction(
    contract_function: ContractFunction,
    value_wei: int = 0,
    wait: bool = True,
    timeout: int = 120,
    poll_latency: int = 2,
) -> Tuple[HexBytes, Optional[TxReceipt]]:

    tx = build_contract_tx(
        contract_function=contract_function,
        value_wei=value_wei,
    )

    tx_hash = sign_and_send_transaction(tx)

    if not wait:
        return tx_hash, None

    receipt = wait_for_receipt(tx_hash, timeout=timeout, poll_latency=poll_latency)
    return tx_hash, receipt
