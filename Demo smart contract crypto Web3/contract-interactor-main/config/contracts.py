# config/contracts.py
from dataclasses import dataclass
from typing import Dict
from config.settings import settings

@dataclass
class ContractConfig:
    name: str
    address: str
    abi_path: str

CONTRACTS: Dict[str, Dict[str, ContractConfig]] = {
    "bsc_testnet": {
        "testToken": ContractConfig(
            name="Lucky Cat Token",
            address="0x450Cd4D19e2c2E18F6A99eDA69e63fc6b0E4944d",
            abi_path="abis/ltc_token.json",
        ),
    },
    "bsc_mainnet": {
        "exampleContract": ContractConfig(
            name="Token name",
            address="Token Address",
            abi_path="abis/example.json",
        ),
    }
}

def get_contract_config(name: str) -> ContractConfig:
    network = settings.network
    network_contracts = CONTRACTS.get(network, {})
    if name not in network_contracts:
        available = ", ".join(network_contracts.keys()) or "<none>"
        raise KeyError(
            f"Contract '{name}' is not configured for network '{network}'. "
            f"Available contracts: {available}"
        )
    return network_contracts[name]
