from typing import Union
from uuid import UUID
from pydantic import BaseModel
from enum import Enum

class TimerStatus(int, Enum):
    waiting = 0
    executing = 1
    done = 2
    failed = 3

class SetTimerResponse(BaseModel):
    id: UUID = ""
    time_left: int


class GetTimerResponse(BaseModel):
    id: UUID = ""
    status: TimerStatus = TimerStatus.waiting 
    time_left: int = 0