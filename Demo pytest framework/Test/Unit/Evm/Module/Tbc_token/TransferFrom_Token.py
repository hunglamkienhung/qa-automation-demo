from Unit.Common.Write_Log import write_log
from Unit.Evm.Module.Assert.BalanceOf import balanceof
from Unit.Evm.Module.Common.Get_ABI_Input import get_abi_input
from Unit.Evm.Module.Common.Call_Contract import call_contract
from Unit.Evm.Models.TransferFrom_Token import TransferFromTokenParams

def transfer_from_token(**kwargs):
    try:
        params_model = TransferFromTokenParams(**kwargs)
        abi_transfer_from=get_abi_input(src_address=params_model.transfer_from_address,approve_to_address=params_model.approve_to_address,transfer_to_address=params_model.transfer_to_address,command_type=params_model.command_type,deploy_contract_address=params_model.deploy_contract_address,amount=str(params_model.amount_transfer_from),token_type=params_model.token_type).json()["result"]
        call_contract(src_address=params_model.approve_to_address,deploy_contract_address=params_model.deploy_contract_address,abi=abi_transfer_from,command_type=params_model.command_type,token_type=params_model.token_type,happy_case=params_model.happy_case)
        balanceof(deploy_contract_address=params_model.deploy_contract_address,src_address=params_model.approve_to_address,balance_of_address=params_model.transfer_to_address,expect_assert=True,expect_amount=params_model.expected,command_type=params_model.command_type,token_type=params_model.token_type)
    except Exception as e:
        write_log(["error", "all"], "error", f"\n❌ Lỗi hệ thống: {e}" + f"\n{'=' * len(str(e))}\n")
        raise e