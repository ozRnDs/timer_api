from fastapi import APIRouter
from uuid import UUID

auto_router = APIRouter(tags=["Tests"])

@auto_router.post("//{timer_id}")
def auto_response_to_timer(timer_id: UUID):
    return {"status": 200, "timer_id": timer_id}