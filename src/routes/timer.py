from fastapi import APIRouter, HTTPException
from uuid import UUID, uuid4
from datetime import datetime, timedelta

from classes.request_objects import SetTimerRequest
from classes.response_objects import GetTimerResponse, TimerStatus, SetTimerResponse

from components.db_api import db_instance, TimerInformation

timers_router = APIRouter(tags=["Timers"])


@timers_router.post("/", 
                    response_model=SetTimerResponse,
                    summary="Create Task With Timer",
                    description="Create new webhook to be activated with timer from now")
def post_timer(timer: SetTimerRequest):
    time_from_now = timedelta(seconds=timer.seconds, hours=timer.hours, minutes=timer.minutes)
    time_to_invoke_url = datetime.now() + time_from_now
    timer_id = db_instance.insert_timer(timer_url=timer.url, timer_invoke_date=time_to_invoke_url)
    return SetTimerResponse(id=timer_id, time_left=time_from_now.seconds)


@timers_router.get("/{timer_id}",
                   response_model=GetTimerResponse,
                   summary="Get Task Status",
                   description="Get task status by it's UUID")
def read_timer(timer_id: UUID):
    timer_information: TimerInformation = db_instance.get_timer_information(str(timer_id))
    if not timer_information:
        raise HTTPException(status_code=404, detail="Task was not found")
    time_left = (timer_information.timer_date - datetime.now()).seconds
    if timer_information.timer_date < datetime.now():
        time_left =0 - (datetime.now()-timer_information.timer_date).seconds
    if timer_information.timer_status != TimerStatus.waiting:
        time_left = 0
    return GetTimerResponse(id=timer_information.timer_id, status=timer_information.timer_status, time_left=time_left)