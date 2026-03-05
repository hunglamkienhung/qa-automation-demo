import pytest
from Setting import path_dir_log
from Unit.Common.Log_Config import log_context
from Unit.Evm.Module.Tbc_token.Approve_Token import approve_token
from Unit.Evm.Module.Tbc_token.Transfer_Token import transfer_token
from Unit.Evm.Module.Tbc_token.TransferFrom_Token import transfer_from_token
from Unit.Evm.Module.Tbc_token.Deploy_Contract import deploy_contract as deploy_func
from Setting import src_addr_list,param_transfer,param_approve,param_transfer_from

@pytest.fixture(scope="session")    # 部署合约
def deploy_contract_address(src_address=src_addr_list[0]):
    return deploy_func(command_type='createContract', token_type='TB-Token', src_address=src_address)

@pytest.fixture(scope="session", autouse=True)
def logging_setup():
    with log_context(path_dir_log): yield  # Giữ log mở trong toàn bộ session

# Tất cả hàm dưới chỉ chạy sau khi deploy_contract chạy xong
@pytest.mark.parametrize('case',param_transfer['transfer'])
def test_transfer_token_after_deploy(case,deploy_contract_address):
    transfer_token( command_type=case['command_type'],transfer_from_address=src_addr_list[case['transfer_from_address_key']],deploy_contract_address=deploy_contract_address,transfer_to_address=src_addr_list[case['transfer_to_address_key']],token_type=case['token_type'],amount_transfer=str(case['amount_transfer']),expected=str(case['expected']),happy_case=case['happy_case'])

@pytest.mark.parametrize('case',param_approve['approve'])
def test_approve_token_after_transfer(case,deploy_contract_address):
    approve_token(command_type=case['command_type'],approve_from_address=src_addr_list[case['approve_from_address_key']],deploy_contract_address=deploy_contract_address,apprrove_to_address=src_addr_list[case['approve_to_address_key']],amount_approve= case['amount_approve'],token_type='TB-Token',happy_case=case['happy_case'])

@pytest.mark.parametrize('case',param_transfer_from['transfer_from'])
def test_transfer_from_token_after_approve(case,deploy_contract_address):
    transfer_from_token(command_type=case['command_type'],transfer_from_address=src_addr_list[case['transfer_from_address_key']],approve_to_address=src_addr_list[case['approve_to_address_key']],transfer_to_address=src_addr_list[case['transfer_to_address_key']],deploy_contract_address=deploy_contract_address,amount_transfer_from=case['amount_transferfrom'],token_type='TB-Token',happy_case=case['happy_case'],expected=str(case['expected']))
