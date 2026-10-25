from sqlalchemy import Column, String, DateTime, Numeric
from database import Base

class PositionPointB(Base):
    __tablename__ = 'position_point_b'
    __table_args__ = {'comment': '가중치 점수 기본'}

    position_cd = Column(String(50), primary_key=True, comment='포지션코드')
    score_cd = Column(String(20), primary_key=True, comment='점수코드')
    position_val = Column(Numeric(10, 4), comment='가중치')
    create_id = Column(String(50), comment='등록자')
    create_dt = Column(DateTime, comment='등록시간')
    update_id = Column(String(50), comment='수정자')
    update_dt = Column(DateTime, comment='수정시간')
