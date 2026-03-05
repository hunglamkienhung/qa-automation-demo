from pydantic import BaseModel, field_validator, Field

# Models Transfer Token
class TransferTokenParams(BaseModel):
    command_type: str
    deploy_contract_address: str = Field(..., min_length=40, max_length=42)
    transfer_from_address: str = Field(..., min_length=40, max_length=42)
    transfer_to_address: str = Field(..., min_length=40, max_length=42)
    amount_transfer: str | int
    token_type: str
    expected: str | int
    happy_case : bool | None = None

    @field_validator('amount_transfer')
    def amount_must_be_numeric(cls, v):
        if not str(v).isdigit():
            raise ValueError("Amount transfer must be numeric string")
        return v
