from Unit.Common.Write_Log import write_log
from Unit.Evm.Module.Common.Write_Log import api_log
from Unit.Common.Requests import api_response
from Unit.Evm.Models.Execute_Contract import CallContractParams
from Setting import url_browser, headers, duration_time_expect

def call_contract(**kwargs):
     try:
        params_model = CallContractParams(**kwargs)
        common_call = 'callContract'
        field_mapping = {'createContract': ('createContract', 'Deploy Contract'),'balanceOf': ('staticCallContract', 'call contract [balance Of]'),**{k: (common_call, f'call contract [{k}]') for k in ['transfer', 'approve', 'transferFrom']}}
        if params_model.command_type not in field_mapping: raise ValueError(f"Unsupported command_type: {params_model.command_type}")
        method , command_str = field_mapping[params_model.command_type]
        data = {
            "method": method,
            "params": {
                "srcaddress": params_model.src_address,
                "amount": 0,
                "contractaddress": params_model.deploy_contract_address,
                "frozen_height": 1,
                "gas": 100000,
                "gas_price": 1,
                "pwd": "123456",
                "comment": params_model.abi
            }
        }
        response_data, duration_time = api_response(url_browser=url_browser, data=data, headers=headers, time_sleep=2,happy_case=params_model.happy_case)
        api_log(happy_case=params_model.happy_case,response_data=response_data,command_type=command_str, duration_time_actual=duration_time, duration_time_expect=duration_time_expect,token_type=params_model.token_type,deploy_contract_address=(response_data.json()["result"]["contract_address"]if params_model.command_type == "createContract" else params_model.deploy_contract_address))
        return response_data
     except Exception as e:
         write_log(["error", "all"], "error", f"\n❌ System error: {e}"+ f"\n{'=' * len(str(e))}\n")
         raise

