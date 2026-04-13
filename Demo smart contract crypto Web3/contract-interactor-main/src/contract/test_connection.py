from config.settings import settings
from src.core.logger import get_logger
from src.core.web3_provider import get_web3

logger = get_logger(__name__)


def main() -> None:
    logger.info(f"Using network: {settings.network}")
    logger.info(f"RPC URL: {settings.rpc_url}")

    web3 = get_web3()

    chain_id = web3.eth.chain_id
    latest_block = web3.eth.block_number

    logger.info(f"Connected chain_id = {chain_id}")
    logger.info(f"Latest block number = {latest_block}")


if __name__ == "__main__":
    main()
