from Unit.Common.Write_Log import write_log
from Unit.Evm.Module.Common.Write_Log import api_log
from Unit.Common.Requests import api_response
from Unit.Evm.Models.Execute_Contract import ABIInputParams
from Setting import url_browser, headers, duration_time_expect

def get_abi_input(**kwargs)-> str:
    try:
        params_model = ABIInputParams(**kwargs)
        field_mapping = {
            "balanceOf": ('address', 'balance Of', f"{params_model.transfer_to_address}"),
            "transfer": ('address-uint256', 'transfer', f"{params_model.transfer_to_address}-{str(params_model.amount)}"),
            "approve": ('address-uint256', 'approve', f"{params_model.transfer_to_address}-{str(params_model.amount)}"),
            "transferFrom": ('address-address-uint256', 'transfer from', f"{params_model.src_address}-{params_model.transfer_to_address}-{str(params_model.amount)}")
        }
        if params_model.command_type not in field_mapping: raise ValueError(f"Unsupported command_type: {params_model.command_type}")
        field_type, command_str, params = field_mapping[params_model.command_type]
        data = {"method": "getabiinput", "params": {"method": params_model.command_type, "field_type": field_type, "params": params}}
        response_data, duration_time = api_response(url_browser=url_browser, data=data, headers=headers)
        api_log(response_data=response_data, command_type=command_str, duration_time_actual=duration_time, duration_time_expect=duration_time_expect,token_type=params_model.token_type,deploy_contract_address=params_model.deploy_contract_address)
        return response_data
    except Exception as e:
        write_log(["error", "all"], "error", f"\n❌ System error: {e}" + f"\n{'=' * len(str(e))}\n")
        raise
