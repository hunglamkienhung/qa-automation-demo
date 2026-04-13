from typing import Any

def get_balance(wallet_address, contract, web3) -> None:

    decimals: int | None
    try:
        decimals_val: Any = contract.functions.decimals().call()
        decimals = int(decimals_val)
    except Exception:
        decimals = None

    if decimals is not None:
        checksum_address = web3.to_checksum_address(wallet_address)
        balance_raw = contract.functions.balanceOf(checksum_address).call()
        human_balance = balance_raw / (10 ** decimals)
        contract_name = contract.functions.name().call()

        print("\n---- RESULT ----\n")
        print(f"\nContract: {contract_name}")
        print(f"Address:  {checksum_address}")
        print(f"Raw balance (base units): {balance_raw}")
        print(f"Readable balance: {human_balance}")
    else:
        print("Decimals: [unknown] (decimals() method not available)")