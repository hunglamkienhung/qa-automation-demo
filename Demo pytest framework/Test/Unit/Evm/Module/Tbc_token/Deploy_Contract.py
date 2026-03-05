from Unit.Common.Write_Log import write_log
from Setting import comment_bytecode
from Unit.Evm.Module.Common.Call_Contract import call_contract
from Unit.Evm.Models.Deploy_Contract import DeployContractParams

def deploy_contract(**kwargs):
    try:
        params_model = DeployContractParams(**kwargs)
        return call_contract(src_address=params_model.src_address,command_type=params_model.command_type,abi=comment_bytecode,token_type=params_model.token_type).json()["result"]["contract_address"]
    except Exception as e:
        write_log(["error", "all"], "error", f"\n❌ System Error: {e}"+ f"\n{'=' * len(str(e))}\n")
        raise SystemExit









