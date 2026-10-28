from sqlalchemy import Column, String, Integer, DateTime, Numeric
from sqlalchemy.orm import declarative_base
# 최상단의 database.py에서 Base를 가져옵니다.
from database import Base

class TeamArrangeL(Base):
    __tablename__ = 'team_arrange_l'
    __table_args__ = {'comment': '팀 배정 리스트'}

    team_uid = Column(String(50), primary_key=True, comment='팀아이디')
    vote_seq = Column(Integer, primary_key=True, comment='투표아이디 (team_schedule_l.vote_seq)')
    member_uid = Column(String(50), primary_key=True, comment='멤버아이디 (용병은 merc_N)')
    member_name = Column(String(50), comment='멤버이름')
    merc_yn = Column(String(1), comment='용병여부 (Y/N)')
    team_no = Column(Integer, comment='배정팀번호 (1:오렌지, 2:그린, 3:블루, 4:핑크)')
    keeper_order = Column(Integer, comment='키퍼순서')
    play_date = Column(String(8), comment='경기일자')
    create_id = Column(String(50), comment='등록자')
    create_dt = Column(DateTime, comment='등록시간')
    update_id = Column(String(50), comment='수정자')
    update_dt = Column(DateTime, comment='수정시간')
