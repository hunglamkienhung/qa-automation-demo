from Unit.Common.Write_Log import write_log
from Unit.Evm.Module.Common.Get_ABI_Input import get_abi_input
from Unit.Evm.Module.Common.Call_Contract import call_contract
from Unit.Evm.Models.TransferFrom_Token import ApproveTokenParams

def approve_token(**kwargs):
    try:
        kwargs_for_model = {k: v for k, v in kwargs.items() if k in ApproveTokenParams.model_fields}
        params_model = ApproveTokenParams(**kwargs_for_model)
        abi_approve=get_abi_input(command_type=params_model.command_type,deploy_contract_address=params_model.deploy_contract_address,transfer_to_address=params_model.apprrove_to_address,amount=str(params_model.amount_approve),token_type=params_model.token_type).json()["result"]
        call_contract(src_address=params_model.approve_from_address,deploy_contract_address=params_model.deploy_contract_address,abi=abi_approve,command_type=params_model.command_type,token_type=params_model.token_type,happy_case=params_model.happy_case)
    except Exception as e:
        write_log(["error", "all"], "error", f"\n❌ Lỗi hệ thống: {e}"+ f"\n{'=' * len(str(e))}\n")
        raise e