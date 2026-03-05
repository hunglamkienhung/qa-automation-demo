from Unit.Common.Write_Log import write_log
from Unit.Evm.Models.Api_Log import ApiLogParams

def api_log(**kwargs):
    try:
        params_model = ApiLogParams(**kwargs)
        load_time = ""
        command_type = params_model.command_type.strip().upper()
        request_data = {
            "method": params_model.response_data.request.method,
            "url": params_model.response_data.request.url,
            "headers": dict(params_model.response_data.request.headers),
            "body": params_model.response_data.request.body.decode() if isinstance(params_model.response_data.request.body, bytes) else params_model.response_data.request.body
        }
        log_msg = f"\n\n📄 {command_type} {params_model.token_type.strip().upper()}\n" + f"\n  📤 REQUEST: {request_data}\n" + f"\n  📥 RESPONSE: {params_model.response_data.text}\n"

        if all(v is not None for v in (params_model.duration_time_actual, params_model.duration_time_expect)):
            load_time = f"\n\n  ⏱️ Response time: Duration_Time_Expect: {params_model.duration_time_expect:.5f}s, Duration_Time_Actual: {params_model.duration_time_actual:.5f}s "
            if params_model.duration_time_actual > params_model.duration_time_expect:load_time += "slower than expected" + f"\n\n{'🐢' * 384}\n"
            else: load_time += "faster than expected" + f"\n\n{'🐇' * 384}\n"
        else: load_time += f"\n\n{'=' * 1024}\n"

        if params_model.response_data.json()["code"] == 2000:
            log_msg += f"\n  ✅ SUCCESSFUL [{command_type}]. Contract address: {params_model.deploy_contract_address}" + load_time
            log_dir = ["all", "pass"]
            if params_model.happy_case is False:
                log_msg += "\n\n ❓ Response code is 2000 — this violates the expectation of a happy case (happy_case = False)\n"
                log_dir=["all","fail"] ; write_log(log_dir, "warning", log_msg)
            else :  write_log(log_dir, "info", log_msg)
        else:
            log_msg += f"\n  ❌ FAILED [{command_type}]." + load_time
            log_dir=["all","pass"]
            if params_model.happy_case is True:
                log_msg +="\n\n ❓ Response code is not 2000 — this violates the expectation of a happy case (happy_case = True)\n"
                log_dir=["all","fail"] ; write_log(log_dir, "warning", log_msg)
            else: write_log(log_dir, "info", log_msg)
        return log_msg
    except Exception as e:
        write_log(["error", "all"], "error", f"\n❌ System error: {e}" + f"\n{'=' * len(str(e))}\n")
        raise e

    # try:
    #     params_model = ApiLogParams(**kwargs)
    #     load_time =""
    #     command_type=params_model.command_type.strip().upper()
    #     request_data = {
    #         "method": params_model.response_data.request.method,
    #         "url": params_model.response_data.request.url,
    #         "headers": dict(params_model.response_data.request.headers),
    #         "body": params_model.response_data.request.body.decode() if isinstance(params_model.response_data.request.body,bytes) else params_model.response_data.request.body
    #     }
    #     log_msg = f"\n\n📄 {command_type} {params_model.token_type.strip().upper()}\n" + f"\n  📤 REQUEST: {request_data}\n" + f"\n  📥 RESPONSE: {params_model.response_data.text}\n"
    #
    #     if all(v is not None for v in (params_model.duration_time_actual, params_model.duration_time_expect)):
    #         load_time = f"\n\n  ⏱️ Response time: Duration_Time_Expect: {params_model.duration_time_expect:.5f}s, Duration_Time_Actual: {params_model.duration_time_actual:.5f}s "
    #         if params_model.duration_time_actual> params_model.duration_time_expect: load_time += "slower than expected" + f"\n\n{'🐢' * 384}\n"
    #         else : load_time += "faster than expected" + f"\n\n{'🐇' * 384}\n"
    #     else: load_time += f"\n\n{'=' * 1024}\n"
    #
    #     if params_model.response_data.json()["code"] == 2000:
    #         log_msg += f"\n  ✅ SUCCESSFUL [{command_type}]. Contract address: {params_model.deploy_contract_address}" + load_time
    #         write_file_txt(filepath=path_dir_log + "\\Pass\\", message=log_msg, file_extension='log')
    #         return log_msg
    #     else:
    #         log_msg += f"\n  ❌ FAILED [{command_type}]." + load_time
    #         write_file_txt(filepath=path_dir_log + "\\Fail\\", message=log_msg, file_extension='log')
    #         return log_msg
    # except Exception as e:
    #     write_file_txt(filepath=path_dir_log+"\\Error\\", message=f"\n❌ Lỗi hệ thống: {e}"+ f"\n{'=' * len(str(e))}\n",file_extension="log")
    #     raise e


