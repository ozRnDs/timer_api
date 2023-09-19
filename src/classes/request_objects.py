from typing import Union
from pydantic import BaseModel, HttpUrl

class SetTimerRequest(BaseModel):
    hours: int = 0
    minutes: int = 0
    seconds: int = 1
    url: HttpUrl | None = None