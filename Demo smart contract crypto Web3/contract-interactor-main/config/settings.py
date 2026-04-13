import os
from dataclasses import dataclass
from typing import Literal
from dotenv import load_dotenv
from networks import BSC_NETWORKS
load_dotenv()
NetworkName = Literal["bsc_mainnet", "bsc_testnet"]

@dataclass
class Settings:
    network: NetworkName
    rpc_url: str
    chain_id: int
    private_key: str
    log_level: str
    gas_price_multiplier: float

    bsc_mainnet_rpc_url: str
    bsc_testnet_rpc_url: str

def _load_settings() -> Settings:
    network = os.getenv("NETWORK", "bsc_testnet")
    if network not in BSC_NETWORKS:
        raise ValueError(
            f"Invalid NETWORK '{network}'. "
            f"Expected one of: {', '.join(BSC_NETWORKS.keys())}"
        )

    bsc_mainnet_rpc_url = os.getenv("BSC_MAINNET_RPC_URL", "").strip()
    bsc_testnet_rpc_url = os.getenv("BSC_TESTNET_RPC_URL", "").strip()

    if not bsc_mainnet_rpc_url:
        pass

    if not bsc_testnet_rpc_url:
        pass

    if network == "bsc_mainnet":
        rpc_url = bsc_mainnet_rpc_url
    else:
        rpc_url = bsc_testnet_rpc_url

    if not rpc_url:
        raise ValueError(
            f"No RPC URL configured for network '{network}'. "
            f"Check your .env (BSC_MAINNET_RPC_URL / BSC_TESTNET_RPC_URL)."
        )

    chain_id = BSC_NETWORKS[network]["chain_id"]
    private_key = os.getenv("PRIVATE_KEY", "").strip()
    if not private_key:
        print("[WARN] PRIVATE_KEY is not set. ")

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    gas_price_multiplier_str = os.getenv("GAS_PRICE_MULTIPLIER", "1.0")
    try:
        gas_price_multiplier = float(gas_price_multiplier_str)
    except ValueError:
        raise ValueError(
            f"GAS_PRICE_MULTIPLIER must be a number, got '{gas_price_multiplier_str}'"
        )

    return Settings(
        network=network,  # type: ignore[arg-type]
        rpc_url=rpc_url,
        chain_id=chain_id,
        private_key=private_key,
        log_level=log_level,
        gas_price_multiplier=gas_price_multiplier,
        bsc_mainnet_rpc_url=bsc_mainnet_rpc_url,
        bsc_testnet_rpc_url=bsc_testnet_rpc_url,
    )
settings = _load_settings()
