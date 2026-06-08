from meta import Base
import datetime
from sqlalchemy import Column, Integer, String, Boolean

class Schedule(Base):
    """
    The Schedule table contains schedule definitons for each jobs.
    When updated, the system will check which schedules are enabled and update the in-memory schedule store accordingly, this is what drives the scheduling of jobs in the system.
    """
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True)
    job_name = Column(String, nullable=False, unique=True) # process/automation/job name
    cron_expr = Column(String, nullable=False) # the schedule as a cron expression
    payload = Column(String, nullable=True)
    enabled = Column(Boolean, nullable=False, default=True)
    created_at = Column(String, nullable=False, default=datetime.datetime.now(datetime.UTC).isoformat())
    updated_at = Column(String, nullable=False, default=datetime.datetime.now(datetime.UTC).isoformat(), onupdate=datetime.datetime.now(datetime.UTC).isoformat())

