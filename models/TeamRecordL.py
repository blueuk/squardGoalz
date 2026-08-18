from sqlalchemy import Column, String, Integer, DateTime, Numeric
from sqlalchemy.orm import declarative_base
# 최상단의 database.py에서 Base를 가져옵니다.
from database import Base

class TeamRecordL(Base):
    __tablename__ = 'team_record_l'
    __table_args__ = {'comment': '팀 기록실 리스트'}

    team_uid = Column(String(50), primary_key=True, comment='팀아이디')
    vote_uid = Column(String(50), primary_key=True, comment='투표아이디')
    play_date = Column(String(8), primary_key=True, comment='경기일자')
    member_uid = Column(String(50), comment='멤버아이디')
    goal_cnt = Column(Integer, comment='골 수')
    asist_cnt = Column(Integer, comment='도움 수')
    create_id = Column(String(50), comment='등록자')
    create_dt = Column(DateTime, comment='등록시간')
    update_id = Column(String(50), comment='수정자')
    update_dt = Column(DateTime, comment='수정시간')