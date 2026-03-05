from Unit.Common.Write_Log import write_log
from Unit.Evm.Module.Assert.BalanceOf import balanceof
from Unit.Evm.Module.Common.Get_ABI_Input import get_abi_input
from Unit.Evm.Module.Common.Call_Contract import call_contract
from Unit.Evm.Models.Transfer_Token import TransferTokenParams

def transfer_token(**kwargs):
    try:
        kwargs_for_model = {k: v for k, v in kwargs.items() if k in TransferTokenParams.model_fields}
        params_model = TransferTokenParams(**kwargs_for_model)
        abi_transfer = get_abi_input(command_type=params_model.command_type,transfer_to_address=params_model.transfer_to_address,amount=str(params_model.amount_transfer),deploy_contract_address=params_model.deploy_contract_address, token_type=params_model.token_type).json()["result"]
        call_contract(src_address=params_model.transfer_from_address,deploy_contract_address=params_model.deploy_contract_address,abi= abi_transfer, command_type=params_model.command_type, token_type=params_model.token_type,happy_case=params_model.happy_case)
        balanceof(deploy_contract_address=params_model.deploy_contract_address,src_address=params_model.transfer_from_address,balance_of_address=params_model.transfer_to_address,expect_assert=True,expect_amount=params_model.expected,command_type=params_model.command_type,token_type=params_model.token_type)
    except Exception as e:
        write_log(["error", "all"], "error", f"\n❌ System error: {e}" + f"\n{'=' * len(str(e))}\n")
        raise e



