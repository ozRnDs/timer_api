from config.config import app_config

from fastapi import FastAPI
import uvicorn

app = FastAPI()

from routes.timer import timers_router
app.include_router(timers_router, prefix="/timer")


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", access_log=False)