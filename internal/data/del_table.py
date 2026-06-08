from sqlalchemy import create_engine, MetaData

engine = create_engine('sqlite:///sample_schedule.db', echo=True)

metadata = MetaData()

metadata.drop_all(engine)