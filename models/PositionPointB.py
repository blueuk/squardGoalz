from sqlalchemy import Column, String, Integer, DateTime, Numeric
from sqlalchemy.orm import declarative_base
# 최상단의 database.py에서 Base를 가져옵니다.
from database import Base

class PositionPointB(Base):
    __tablename__ = 'position_point_b'
    __table_args__ = {'comment': '가중치 점수 기본'}

    position_cd = Column(String(50),  comment='포지션코드')
    score_cd = Column(String(20), primary_key=True, comment='점수코드 (시트 2 참조)')
    position_val = Column(Numeric, comment='점수')
    create_id = Column(String(50), comment='등록자')
    create_dt = Column(DateTime, comment='등록시간')
    update_id = Column(String(50), comment='수정자')
    update_dt = Column(DateTime, comment='수정시간')