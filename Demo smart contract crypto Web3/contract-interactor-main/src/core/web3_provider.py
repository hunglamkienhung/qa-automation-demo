from typing import Optional

from web3 import Web3

from config.settings import settings
from src.core.logger import get_logger

logger = get_logger(__name__)

_web3_instance: Optional[Web3] = None


def get_web3() -> Web3:
    global _web3_instance

    if _web3_instance is None:
        logger.info(
            f"Initializing Web3 provider for network={settings.network}, "
            f"rpc_url={settings.rpc_url}"
        )
        _web3_instance = Web3(Web3.HTTPProvider(settings.rpc_url))

        if not _web3_instance.is_connected():
            raise ConnectionError(
                f"Failed to connect to RPC at {settings.rpc_url}. "
                "Check your RPC URL and network connectivity."
            )

        try:
            chain_id = _web3_instance.eth.chain_id
            latest_block = _web3_instance.eth.block_number
            logger.info(
                f"Connected to chain_id={chain_id}, latest_block={latest_block}"
            )
        except Exception as e:
            logger.warning(f"Connected, but failed to fetch chain info: {e}")

    return _web3_instance
