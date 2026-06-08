import asyncio
from dataclasses import dataclass

@dataclass
class ScheduleEntry:
    id:            int
    job_name:      str
    cron_expr:     str
    payload:       dict
    enabled:       bool

class ScheduleStore:
    def __init__(self, db_session):
        self._schedules: dict[int, ScheduleEntry] = {}
        self._lock =  asyncio.Lock()
    
    async def load(self, entries: list[ScheduleEntry]):
        async with self._lock:
            self._schedules = {entry.id: entry for entry in entries}
    
    async def get_enabled(self) -> list[ScheduleEntry]:
        # List all enabled schedules from the database
        async with self._lock:
            return [entry for entry in self._schedules.values() if entry.enabled]

    async def upsert(self, entry: ScheduleEntry):
        # Add or update schedule in the database
        async with self._lock:
            self._schedules[entry.id] = entry

    async def remove(self, entry: ScheduleEntry):
        # Remove schedule from the database
        async with self._lock:
            self._schedules.pop(entry.id, None)


