from config.config import app_config

from fastapi import FastAPI
import uvicorn

app = FastAPI(description="Rest API Interface for the timer service")

from routes.timer import timers_router
app.include_router(timers_router, prefix="/timer")

from routes.auto_response import auto_router
app.include_router(auto_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", access_log=False)