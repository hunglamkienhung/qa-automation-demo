from typing import Any
from pydantic import BaseModel, model_validator

class ApiLogParams(BaseModel):
    response_data: Any
    command_type: str
    duration_time_actual: float | None = None
    duration_time_expect: float | None = None
    token_type: str = ''
    deploy_contract_address: str | None = None
    happy_case: bool | None = None

    @model_validator(mode="after")
    def validate_fields(self) -> "ApiLogParams":
        if self.command_type != 'createContract' and not self.deploy_contract_address:
            raise ValueError("deploy_contract_address is required unless command_type is 'createContract'")
        return self