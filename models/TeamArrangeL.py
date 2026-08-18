from sqlalchemy import Column, String, Integer, DateTime, Numeric
from sqlalchemy.orm import declarative_base
# 최상단의 database.py에서 Base를 가져옵니다.
from database import Base

class TeamArrangeL(Base):
    __tablename__ = 'team_arrange_l'
    __table_args__ = {'comment': '팀 배정 리스트'}

    vote_uid = Column(String(50), primary_key=True, comment='투표아이디')
    play_date = Column(String(8), comment='경기일자')
    team_cd = Column(String(20), comment='팀구분코드')
    member_id = Column(String(50), comment='멤버아이디')
    create_id = Column(String(50), comment='등록자')
    create_dt = Column(DateTime, comment='등록시간')
    update_id = Column(String(50), comment='수정자')
    update_dt = Column(DateTime, comment='수정시간')