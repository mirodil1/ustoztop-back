from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()


def init_db():
    import models

    Base.metadata.create_all(bind=engine)

