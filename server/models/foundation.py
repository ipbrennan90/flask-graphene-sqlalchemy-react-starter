from sqlalchemy import *
from sqlalchemy.orm import (
    scoped_session, sessionmaker, relationship, backref)

from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://iam:developer@db:5432/school')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()

Base.query = db_session.query_property()
