from meta import Base
from sqlalchemy import Column, Integer, String, JSON, DateTime, CheckConstraint

valid_statuses = [
    "pending",      # waiting for dependencies
    "ready",        # ready to be worked
    "running",      # is being worked
    "completed",    # done
    "failed",       # finished with error
    "canceled"      # removed
]

class Job(Base):
    """
    Defintition of a Job that can be queued and worked on.
    
    """
    __tablename__ = "jobs"

    id                   = Column(Integer, primary_key=True)
    name                 = Column(String, nullable=False)
    payload              = Column(JSON, nullable=True)
    status               = Column(String, default="ready")   # see statuses above
    depends_on           = Column(JSON, nullable=True)        # list of job IDs, null = no deps
    on_dependency_failure = Column(String, default="cascade_cancel")
    enqueued_at          = Column(DateTime(timezone=True))
    started_at           = Column(DateTime(timezone=True), nullable=True)
    completed_at         = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint(status.in_(valid_statuses), name="check_valid_status")
    )