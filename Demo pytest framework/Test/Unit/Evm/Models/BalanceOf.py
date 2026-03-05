from pydantic import BaseModel, field_validator, Field, model_validator

class BalanceOfParams(BaseModel):
    deploy_contract_address: str = Field(min_length=40, max_length=42)  # luôn bắt buộc
    src_address: str = Field(min_length=40, max_length=42)
    balance_of_address: str | None = Field( min_length=40, max_length=42)
    expect_assert: bool = Field(default=True, alias="assert")
    expect_amount: str | int | None = None
    command_type:str
    token_type: str
    happy_case: bool | None = None

    @field_validator('expect_amount')
    @classmethod
    def amount_must_be_numeric(cls, v):
        if v is not None and not str(v).isdigit():
            raise ValueError("Amount must be numeric string")
        return v