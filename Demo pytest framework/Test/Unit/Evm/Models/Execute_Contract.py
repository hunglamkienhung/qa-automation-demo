from typing import Literal
from pydantic import BaseModel, field_validator, Field, model_validator

# Model: Get ABI Input
class ABIInputParams(BaseModel):
    command_type: Literal["balanceOf", "transfer", "approve", "transferFrom"]
    src_address: str = Field(default=None, min_length=40, max_length=42, description="transferfrom_from_address OR approve_to_address")
    amount: str | int | None = None
    token_type: str
    transfer_to_address: str | None = Field(default=None, min_length=40, max_length=42,description="balanceOf_address")
    deploy_contract_address: str = Field(..., min_length=40, max_length=42)  # luôn bắt buộc

    @field_validator('amount')
    @classmethod
    def amount_must_be_numeric(cls, v):
        if v is not None and not str(v).isdigit():
            raise ValueError("Amount must be numeric string")
        return v

# Model: Call Contract
class CallContractParams(BaseModel):
    command_type: str
    src_address: str = Field(default=None, min_length=40, max_length=42, description="transfer_form_address OR balanceOf_address OR apprrove_to_address")
    deploy_contract_address: str | None = Field(default=None, min_length=40, max_length=42)
    abi: str
    token_type: str
    happy_case: bool | None = None

    @model_validator(mode="after")
    def validate_fields(self) -> "CallContractParams":
        if self.command_type not in ('createContract', 'Deploy Contract') and not self.deploy_contract_address:
            raise ValueError("deploy_contract_address is required unless command_type is 'createContract' or 'Deploy Contract'")
        return self

# Model: Contract Group
class ContractModel(BaseModel):
    abi_input_params: ABIInputParams | None = None
    call_contract_params: CallContractParams | None = None
