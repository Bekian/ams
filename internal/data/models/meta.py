from sqlalchemy.orm import DeclarativeBase

# base class for all models, all models will be loaded using this base class.
class Base(DeclarativeBase):
    pass
