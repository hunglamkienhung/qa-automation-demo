# src/blockchain/contract_loader.py

import json
from pathlib import Path
from typing import Any, Dict, List, Union

from web3 import Web3

try:
    from web3.contract.contract import Contract
except ImportError:
    from web3.contract import Contract  # type: ignore[attr-defined]

from config.contracts import get_contract_config, ContractConfig
from config.settings import settings
from src.core.logger import get_logger
from src.core.web3_provider import get_web3
from src.core.exceptions import ContractLoadError

logger = get_logger(__name__)

AbiType = List[Dict[str, Any]]
AbiInputOutput = List[Dict[str, Any]]


def _parse_abi(abi: Union[str, AbiType]) -> AbiType:

    if isinstance(abi, list):
        return abi

    s = abi.strip()

    # Try parse as JSON text
    if s.startswith("["):
        try:
            parsed = json.loads(s)
            if isinstance(parsed, list):
                return parsed  # type: ignore[return-value]
        except json.JSONDecodeError as e:
            raise ContractLoadError(f"Failed to parse ABI JSON string: {e}")

    # Otherwise, treat as file path
    path = Path(s)
    if not path.is_file():
        raise ContractLoadError(
            f"ABI string is neither valid JSON nor an existing file path: {s}"
        )

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise ContractLoadError(f"Failed to read ABI from file {path}: {e}")

    if not isinstance(data, list):
        raise ContractLoadError(f"ABI file {path} does not contain a JSON list")

    return data  # type: ignore[return-value]

def load_contract(web3: Web3 | None = None, contract_name: str | None = None) -> Contract:

    cfg = get_contract_config(contract_name)
    address = cfg.address
    abi = cfg.abi_path
    if web3 is None:
        web3 = get_web3()

    try:
        checksum_address = web3.to_checksum_address(address)
    except Exception as e:
        raise ContractLoadError(f"Invalid contract address '{address}': {e}")

    parsed_abi = _parse_abi(abi)

    try:
        contract = web3.eth.contract(address=checksum_address, abi=parsed_abi)
    except Exception as e:
        raise ContractLoadError(f"Failed to create contract instance: {e}")

    logger.info(f"Loaded contract at {checksum_address}")
    return contract


def list_contract_methods(contract: Contract) -> Dict[str, List[Dict[str, Any]]]:

    all_methods: List[Dict[str, Any]] = []

    for item in contract.abi:
        if item.get("type") != "function":
            continue

        method_info = {
            "name": item.get("name"),
            "inputs": item.get("inputs", []),
            "outputs": item.get("outputs", []),
            "stateMutability": item.get("stateMutability", "nonpayable"),
        }
        all_methods.append(method_info)

    read_only = [
        m for m in all_methods if m["stateMutability"] in ("view", "pure")
    ]
    write = [
        m for m in all_methods if m["stateMutability"] in ("nonpayable", "payable")
    ]

    logger.debug(
        f"Contract methods: total={len(all_methods)}, "
        f"read_only={len(read_only)}, write={len(write)}"
    )

    return {
        "all": all_methods,
        "read_only": read_only,
        "write": write,
    }


def load_named_contract(
    name: str,
    web3: Web3 | None = None,
) -> Contract:

    cfg: ContractConfig = get_contract_config(name)
    logger.info(
        f"Loading named contract '{name}' for network={settings.network} "
        f"at address={cfg.address}, abi_path={cfg.abi_path}"
    )

    contract = load_contract(
        address=cfg.address,
        abi=cfg.abi_path,  # treated as file path by _parse_abi
        web3=web3,
    )
    return contract
