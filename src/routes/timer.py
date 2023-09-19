from fastapi import APIRouter
from uuid import UUID, uuid4
from datetime import datetime, timedelta

from classes.request_objects import SetTimerRequest
from classes.response_objects import GetTimerResponse, TimerStatus, SetTimerResponse

from components.db_api import db_instance, TimerInformation

timers_router = APIRouter()


@timers_router.post("/")
def post_timer(timer: SetTimerRequest):
    time_from_now = timedelta(seconds=timer.seconds, hours=timer.hours, minutes=timer.minutes)
    time_to_invoke_url = datetime.now() + time_from_now
    timer_id = db_instance.insert_timer(timer_url=timer.url, timer_invoke_date=time_to_invoke_url)
    return SetTimerResponse(id=timer_id, time_left=time_from_now.seconds)


@timers_router.get("/{timer_id}")
def read_timer(timer_id: UUID):
    timer_information: TimerInformation = db_instance.get_timer_information(str(timer_id))
    time_left = timer_information.timer_date - datetime.now()
    return GetTimerResponse(id=timer_information.timer_id, status=timer_information.timer_status, time_left=time_left.seconds)