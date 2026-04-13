# src/blockchain/account_manager.py

from dataclasses import dataclass
from typing import Optional, Literal, Any

from eth_account.signers.local import LocalAccount
from eth_account.datastructures import SignedTransaction

from web3 import Web3
from web3.types import TxParams, ChecksumAddress

from config.settings import settings
from src.core.logger import get_logger
from src.core.web3_provider import get_web3
from src.core.exceptions import TransactionError

logger = get_logger(__name__)

_account_manager: Optional["AccountManager"] = None


@dataclass
class AccountManager:

    web3: Web3
    account: LocalAccount

    @property
    def address(self) -> ChecksumAddress:
        return self.account.address

    def get_nonce(self, use_pending: bool = True) -> int:
        block_tag: Literal["pending", "latest"] = (
            "pending" if use_pending else "latest"
        )

        nonce = self.web3.eth.get_transaction_count(self.address, block_tag)
        logger.debug(f"Nonce for {self.address} at {block_tag}: {nonce}")
        return nonce

    def sign_transaction(self, tx: TxParams) -> "SignedTransaction":

        tx_dict: dict[str, Any] = dict(tx)
        logger.debug(f"Signing transaction: {tx}")
        return self.account.sign_transaction(tx_dict)


def get_account_manager() -> AccountManager:

    global _account_manager

    if _account_manager is None:
        if not settings.private_key:
            raise TransactionError(
                "PRIVATE_KEY is not set. Cannot create AccountManager."
            )

        web3 = get_web3()

        try:
            account: LocalAccount = web3.eth.account.from_key(settings.private_key)
        except Exception as e:
            raise TransactionError(f"Invalid PRIVATE_KEY: {e}")

        logger.info(f"Loaded account with address {account.address}")
        _account_manager = AccountManager(web3=web3, account=account)

    return _account_manager


# ------------use below code when you want to get_account_manager()
# from src.blockchain.account_manager import get_account_manager
#
# am = get_account_manager()
# print(am.address)
# nonce = am.get_nonce()
