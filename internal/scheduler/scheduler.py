import asyncio
import logging
from datetime import datetime, timezone

from croniter import croniter

from internal.data.store import ScheduleStore, ScheduleEntry

logger = logging.getLogger(__name__)

MAX_SLEEP = 60.0  # re-evaluate at least every 60s


def compute_next_run(cron_expr: str, base: datetime | None = None) -> datetime:
    base = base or datetime.now(timezone.utc)
    return croniter(cron_expr, base).get_next(datetime).replace(tzinfo=timezone.utc)


class SchedulerLoop:
    def __init__(self, store: ScheduleStore, worker_client: WorkerClient):
        self.store = store
        self.worker_client = worker_client
        self._task: asyncio.Task | None = None
        self._wakeup = asyncio.Event()

    async def start(self) -> None:
        self._task = asyncio.create_task(self._loop(), name="scheduler-loop")
        logger.info("Scheduler loop started")

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Scheduler loop stopped")

    def notify(self) -> None:
        """Wake the loop early — call this after any schedule mutation."""
        self._wakeup.set()

    async def _loop(self) -> None:
        while True:
            now = datetime.now(timezone.utc)
            next_wake: datetime | None = None

            for schedule in await self.store.get_enabled():
                if schedule.next_run <= now:
                    asyncio.create_task(self._fire(schedule))
                    new_next = compute_next_run(schedule.cron_expr, now)
                else:
                    if next_wake is None or schedule.next_run < next_wake:
                        next_wake = schedule.next_run

            delay = MAX_SLEEP
            if next_wake is not None:
                delay = min((next_wake - datetime.now(timezone.utc)).total_seconds(), MAX_SLEEP)
            delay = max(delay, 0)

            self._wakeup.clear()
            try:
                await asyncio.wait_for(self._wakeup.wait(), timeout=delay)
            except asyncio.TimeoutError:
                pass  # normal — woke up on schedule

    async def _fire(self, schedule: ScheduleEntry) -> None:
        logger.info(f"Firing schedule {schedule.id} → automation {schedule.automation_id}")
        try:
            await self.worker_client.run(schedule.automation_id, schedule.payload or {})
        except Exception:
            logger.exception(f"Failed to fire schedule {schedule.id}")