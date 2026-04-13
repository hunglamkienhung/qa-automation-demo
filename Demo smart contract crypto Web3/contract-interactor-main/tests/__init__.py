from src.contract.get_balance_simple import*
from web3 import Web3
from config.settings import settings
from src.blockchain.contract_loader import load_contract


def setup():
    wallet_address = "0x385eea48314f1238ea4aac4984a24f453d16b0cf"
    contract_name = "testToken"
    web3 = Web3(Web3.HTTPProvider(settings.rpc_url))
    contract = load_contract(contract_name=contract_name, web3=web3)
    return web3, contract, wallet_address

def main()->None:
    web3, contract, wallet_address = setup()
    get_balance(wallet_address, contract, web3)

if __name__ == "__main__":
    main()
