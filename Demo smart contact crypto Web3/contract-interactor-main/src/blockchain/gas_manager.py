# src/blockchain/gas_manager.py

from typing import Optional

from web3 import Web3
# from web3.contract.contract import ContractFunction

try:
    from web3.contract.contract import ContractFunction
except ImportError:
    from web3.contract import ContractFunction

from config.settings import settings
from src.core.logger import get_logger

logger = get_logger(__name__)


def get_gas_price(web3: Web3, multiplier: Optional[float] = None) -> int:

    base_price = web3.eth.gas_price

    m = multiplier if multiplier is not None else settings.gas_price_multiplier
    gas_price = int(base_price * m)

    logger.debug(
        f"Base gas price: {base_price} wei, multiplier={m} -> gas_price={gas_price} wei"
    )
    return gas_price


def estimate_gas_for_function(
    contract_function: ContractFunction,
    from_address: str,
    value_wei: int = 0,
) -> int:

    tx_params = {
        "from": from_address,
        "value": value_wei,
    }

    # Web3.py v6 uses estimate_gas; some older code used estimateGas.

    try:
        gas_estimate = contract_function.estimate_gas(tx_params)
    except AttributeError:
        gas_estimate = contract_function.estimateGas(tx_params)

    logger.debug(
        f"Gas estimate for {getattr(contract_function, 'fn_name', '<fn>')} "
        f"from {from_address}: {gas_estimate}"
    )
    return gas_estimate
