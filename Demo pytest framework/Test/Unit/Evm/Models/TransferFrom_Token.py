from pydantic import BaseModel, field_validator, Field

# Models Approve Token
class ApproveTokenParams(BaseModel):
    command_type: str
    deploy_contract_address: str = Field(..., min_length=40, max_length=42)
    approve_from_address: str = Field(..., min_length=40, max_length=42)
    apprrove_to_address: str = Field(..., min_length=40, max_length=42)
    amount_approve: str | int
    token_type: str
    happy_case: bool | None = None

    @field_validator('amount_approve')
    def amount_must_be_numeric(cls, v):
        if not str(v).isdigit():
            raise ValueError("Amount approve must be numeric string")
        return v

# Models Transfer From Token
class TransferFromTokenParams(BaseModel):
    approve_to_address: str = Field(..., min_length=40, max_length=42)
    command_type: str
    deploy_contract_address: str = Field(..., min_length=40, max_length=42)
    transfer_from_address: str = Field(..., min_length=40, max_length=42)
    transfer_to_address: str = Field(..., min_length=40, max_length=42)
    amount_transfer_from: str | int  # dùng str để dễ kiểm tra validator
    token_type: str
    expected: str | int
    happy_case: bool

    @field_validator('amount_transfer_from')
    def amount_must_be_numeric(cls, v):
        if not str(v).isdigit():
            raise ValueError("Amount transfer_from must be numeric string")
        return v

    @field_validator('expected')
    def amount_must_be_numeric(cls, v):
        if not str(v).isdigit():
            raise ValueError("Expected transfer must be numeric string")
        return v

# All Models For Class
class TransferModel(BaseModel):
    approve_params: ApproveTokenParams | None = None
    transferFrom_params: TransferFromTokenParams | None = None
