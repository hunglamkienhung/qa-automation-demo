from typing import Any
from web3 import Web3
from config.settings import settings
from src.blockchain.contract_loader import load_contract
from web3.types import TxParams


def transfer(receiver, amount) -> None:

    contract_name = "testToken"
    web3 = Web3(Web3.HTTPProvider(settings.rpc_url))
    contract = load_contract(contract_name=contract_name, web3=web3)
    private_key = settings.private_key
    account = web3.eth.account.from_key(private_key)
    sender = account.address
    receiver = web3.to_checksum_address(receiver)
    amount = amount

    fn = contract.functions.transfer(receiver, amount)
    nonce = web3.eth.get_transaction_count(sender, "pending")
    gas_estimate = fn.estimate_gas({"from": sender})
    gas_price = web3.eth.gas_price

    decimals: int | None
    decimals_val: Any = contract.functions.decimals().call()
    decimals = int(decimals_val)

    tx: TxParams = {
        "from": sender,
        "nonce": nonce,
        "gas": gas_estimate,
        "gasPrice": gas_price,
        "chainId": settings.chain_id,
        "value": 0,
    }

    tx = fn.build_transaction(tx)
    signed = account.sign_transaction(tx)
    tx_hash = web3.eth.send_raw_transaction(signed.raw_transaction)

    print(f"Sender:    {sender}")
    print(f"receiver:    {receiver}\n")

    print("Building transaction…")
    print(f"  nonce:     {nonce}")
    print(f"  gas:       {gas_estimate}")
    print(f"  gasPrice:  {gas_price}")
    print(f"  amount:      {amount/ (10 ** decimals)}\n")

    print("Sending transaction…")

    print("\n---- RESULT ----")
    print(f"TX HASH: {tx_hash.hex()}")

def main():
    receiver = "0xba55b3d4a54793a7e487e1ca3f0f7c2e109c0600"
    amount = 1_000_000_000_000_000_000
    transfer(receiver, amount)


if __name__ == "__main__":
    main()
