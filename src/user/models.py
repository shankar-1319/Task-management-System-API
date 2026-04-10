from sqlalchemy import Column,String,Boolean,Integer,DateTime,func
from src.utils.db import Base

class UserModel(Base):
    __tablename__="user_table"

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String,nullable=False)
    username = Column(String,nullable=False)
    hashed_password = Column(String,nullable=False)
    email = Column(String)
    phone = Column(String)
    create_time_date = Column(DateTime,default=func.now())