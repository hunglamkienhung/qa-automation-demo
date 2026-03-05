import time
import requests
from typing import Any, Dict
from pydantic import BaseModel, AnyUrl, field_validator

class Model(BaseModel):
    url_browser: AnyUrl | str
    data: Dict[str, Any]
    headers: Dict[str, str]
    time_sleep: str | int | float | None = 0

    @field_validator('time_sleep')
    def amount_must_be_numeric(cls, v):
        if not str(v).isdigit():
            raise ValueError("Amount transfer must be numeric string")
        return v

def api_response(**kwargs):
    params_model = Model(**kwargs)
    start_time = time.perf_counter()
    try: response_data = requests.post(url=params_model.url_browser,json=params_model.data,headers=params_model.headers);
    finally:
        duration_time = time.perf_counter() - start_time
        time.sleep(params_model.time_sleep)
    return response_data, duration_time


