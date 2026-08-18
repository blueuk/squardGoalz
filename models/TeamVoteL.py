from sqlalchemy import Column, String, Integer, DateTime, Numeric
from sqlalchemy.orm import declarative_base
# 최상단의 database.py에서 Base를 가져옵니다.
from database import Base

class TeamVoteL(Base):
    __tablename__ = 'team_vote_l'
    __table_args__ = {'comment': '팀 투표 리스트'}

    vote_seq = Column(Integer, primary_key=True, comment='투표아이디')
    team_uid = Column(String(50), primary_key=True, comment='팀아이디')
    play_date = Column(String(8), comment='경기일자')
    play_start_time = Column(String(10), comment='경기시작시간')
    play_end_time = Column(String(10), comment='경기종료시간')
    member_uid = Column(String(50), comment='멤버아이디')
    vote_cd = Column(String(20), comment='투표코드')
    create_id = Column(String(50), comment='등록자')
    create_dt = Column(DateTime, comment='등록시간')
    update_id = Column(String(50), comment='수정자')
    update_dt = Column(DateTime, comment='수정시간')