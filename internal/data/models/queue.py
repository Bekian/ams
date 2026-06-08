from meta import Base
import datetime
from sqlalchemy import Column, Integer, String
from job import Job

class Queue(Base):
    """
    Table of queued jobs that will be and have been processed. 
    This is the main table that the system operates on - jobs are added here, workers pick them up, and their status is updated here. 
    Once a job is completed, this becomes a historical record of what was processed and when, this can be very powerful when paired with the logging table.
    """
    __tablename__ = 'queue'

    id = Column(Integer, primary_key=True, autoincrement=True) # Queue Item ID, auto-incrementing
    job_id = Column(Integer, nullable=False) # reference to the Job table, for details on the job being processed
    job_name = Column(String, nullable=False) # process/automation/job name
    payload = Column(String, nullable=True)
    correlation_id = Column(String, nullable=False) # for tracking related jobs across the system
    created_at = Column(String, nullable=False, default=datetime.datetime.now(datetime.UTC).isoformat()) # when the job was added to the queue
    started_at = Column(String, nullable=True) # when the job was picked up by a worker, null if not picked up yet
    completed_at = Column(String, nullable=True) # when the job was completed, null if not completed yet
    updated_at = Column(String, nullable=False, default=datetime.datetime.now(datetime.UTC).isoformat(), onupdate=datetime.datetime.now(datetime.UTC).isoformat()) # updated when the status is changed