from sqlalchemy import Column, String, Integer, DateTime, Numeric
from sqlalchemy.orm import declarative_base
# 최상단의 database.py에서 Base를 가져옵니다.
from database import Base

class TeamMemberL(Base):
    __tablename__ = 'team_member_l'
    __table_args__ = {'comment': '팀 멤버 리스트'}

    team_uid = Column(String(50), primary_key=True, comment='팀아이디')
    member_uid = Column(String(50), primary_key=True, comment='멤버아이디')
    member_name = Column(String(50), comment='멤버이름')
    user_id = Column(String(50), comment='유저아이디')
    sign_dt = Column(String(14), comment='가입일자')
    gender_cd = Column(String(10), comment='성별 (01:남자, 02: 여자)')
    status_cd = Column(String(10), comment='상태 (01: 활동, 02: 부상, 03: 휴식)')
    terminate_dt = Column(String(14), comment='탈퇴일자')
    create_id = Column(String(50), comment='등록자')
    create_dt = Column(DateTime, comment='등록시간')