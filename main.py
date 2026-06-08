from fastapi import FastAPI
from automation_router import epa_router, ga_router
import uvicorn
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    await load_schedules_from_db()  # hydrate APScheduler from DB
    yield
    scheduler.shutdown()

async def load_schedules_from_db():
    schedules = await db.fetch_all("SELECT * FROM schedules WHERE enabled = 1")
    for schedule in schedules:
        add_to_scheduler(schedule)

app = FastAPI(title="api-worker-demo-service", lifespan=lifespan)

app.include_router(epa_router)
app.include_router(ga_router)


def main():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")


if __name__ == "__main__":
    main()
