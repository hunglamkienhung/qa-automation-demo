# src/contract/list_read_methods.py

import argparse

from src.core.logger import get_logger
from src.blockchain.contract_loader import load_named_contract, list_contract_methods

logger = get_logger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="List read-only methods of a named contract."
    )
    parser.add_argument(
        "--contract",
        "-c",
        default="testToken",
        help="Logical contract name as defined in config/contracts.py (default: testToken)",
    )

    args = parser.parse_args()
    contract_name: str = args.contract

    logger.info(f"Loading contract '{contract_name}'...")
    contract = load_named_contract(contract_name)

    methods_info = list_contract_methods(contract)
    read_only_methods = methods_info.get("read_only", [])

    print(f"\nRead-only methods for contract '{contract_name}':\n")

    if not read_only_methods:
        print("  (No read-only methods found)")
        return

    for m in read_only_methods:
        name = m["name"]
        state = m["stateMutability"]
        inputs = m["inputs"]
        outputs = m["outputs"]

        # Format inputs and outputs nicely
        in_sig = ", ".join(f"{i['type']} {i.get('name', '')}".strip() for i in inputs)
        out_sig = ", ".join(f"{o['type']} {o.get('name', '')}".strip() for o in outputs)

        print(f"- {name}()")
        print(f"    stateMutability: {state}")
        print(f"    inputs:  ({in_sig})" if inputs else "    inputs:  ()")
        print(f"    outputs: ({out_sig})" if outputs else "    outputs: ()")
        print()


if __name__ == "__main__":
    main()
