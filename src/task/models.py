from sqlalchemy import Column, String, Boolean, Integer,ForeignKey
from src.utils.db import Base

class TaskModel(Base):
    __tablename__ = "user_task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    status = Column(Boolean, default=False)

    user_id = Column(Integer,ForeignKey("user_table.id",ondelete="CASCADE"))
