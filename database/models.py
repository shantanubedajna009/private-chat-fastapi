from datetime import datetime
from sqlite3 import Timestamp
from database.db import Base
from sqlalchemy import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer, String, DateTime

class DbUser(Base):
    __tablename__   = 'users'
    id              = Column(Integer, primary_key=True, index=True) 
    username        = Column(String)
    email           = Column(String)
    password        = Column(String)
    date_created    = Column(DateTime)