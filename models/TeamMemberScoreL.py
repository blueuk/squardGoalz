from sqlalchemy import Column, String, Integer, DateTime, Numeric
from sqlalchemy.orm import declarative_base
# 최상단의 database.py에서 Base를 가져옵니다.
from database import Base

class TeamMemberScoreL(Base):
    __tablename__ = 'team_member_score_l'
    __table_args__ = {'comment': '팀 점수 리스트'}

    member_uid = Column(String(50), primary_key=True, comment='멤버아이디')
    team_uid = Column(String(50), primary_key=True, comment='팀아이디')
    year = Column(String(4), primary_key=True, comment='년도')
    score_cd = Column(String(20), primary_key=True, comment='점수코드 (시트 2 참조)')
    score_val = Column(Numeric, comment='점수')
    create_id = Column(String(50), comment='등록자')
    create_dt = Column(DateTime, comment='등록시간')
    update_id = Column(String(50), comment='수정자')
    update_dt = Column(DateTime, comment='수정시간')