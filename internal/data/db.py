from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.meta import Base

DATABASE_URL = 'sqlite:///sample_schedule.db'

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_session():
    return SessionLocal()