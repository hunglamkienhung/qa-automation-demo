from pydantic import BaseModel, Field

class DeployContractParams(BaseModel):
    command_type: str
    src_address: str = Field(default=None, min_length=40, max_length=42)
    token_type: str