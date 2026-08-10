from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
# 최상단의 database.py에서 Base를 가져옵니다.
from database import Base

class User(Base):
    __tablename__ = "sqg_users"

    userid = Column(String, primary_key=True, index=True)
    password = Column(String, nullable=False)
    username = Column(String, nullable=False)
    created_dt = Column(DateTime, server_default=func.now())