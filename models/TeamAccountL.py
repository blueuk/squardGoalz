from sqlalchemy import Column, String, Integer, DateTime, Numeric
from sqlalchemy.orm import declarative_base
# 최상단의 database.py에서 Base를 가져옵니다.
from database import Base

class TeamAccountL(Base):
    __tablename__ = 'team_account_l'
    __table_args__ = {'comment': '팀 계좌 리스트'}

    team_uid = Column(String(50), primary_key=True, comment='팀아이디')
    team_account_seq = Column(Integer, primary_key=True, autoincrement=True, comment='시퀀스')
    bank_cd = Column(String(20), primary_key=True, comment='은행코드')
    account_enc = Column(String(255), primary_key=True, comment='계좌번호')
    create_id = Column(String(50), comment='등록자')
    create_dt = Column(DateTime, comment='등록시간')
    update_id = Column(String(50), comment='수정자')
    update_dt = Column(DateTime, comment='수정시간')