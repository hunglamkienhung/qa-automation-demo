from Unit.Evm.Models.BalanceOf import BalanceOfParams
from Unit.Evm.Module.Common.Get_ABI_Input import get_abi_input
from Unit.Evm.Module.Common.Call_Contract import call_contract
from Unit.Common.Write_Log import write_log

def balanceof(**kwargs):
    try:
        params_model = BalanceOfParams(**kwargs)
        abi_balanceOf = get_abi_input(command_type='balanceOf', transfer_to_address=params_model.balance_of_address,token_type=params_model.token_type,deploy_contract_address=params_model.deploy_contract_address).json()["result"]
        balanceOf_callContract = call_contract(src_address=params_model.src_address, command_type='balanceOf',deploy_contract_address=params_model.deploy_contract_address,abi=abi_balanceOf, token_type=params_model.token_type)

        if params_model.expect_assert != True: return balanceOf_callContract
        if(balanceOf_callContract.json()["code"] == 2000):
            balance = int(balanceOf_callContract.json()["result"], 16)
            log_message = f"Expected: {str(params_model.expect_amount)}, Actual: {str(balance)}\n\n{'🎉' * 1024}\n"
            if int(params_model.expect_amount) == balance:
                write_log(["pass", "all"], "info", f"\n\n 🎯  🟢🟢🟢🟢🟢 match ⏩ "f"{log_message} \n")
            else :
                write_log(["pass", "all"], "info", f"\n\n 🎯  🔴🔴🔴🔴🔴 match ⏩ "f"{log_message} \n")
        else:
            write_log(["fail", "all"], "warning", f"\n  ❌ FAILED.")

    except Exception as e:
        write_log(["error", "all"], "info", f"\n❌ Lỗi hệ thống: {e}" + f"\n{'=' * len(str(e))}\n")
        raise e