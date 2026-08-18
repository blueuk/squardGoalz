from sqlalchemy import Column, String, Integer, DateTime, Numeric
from sqlalchemy.orm import declarative_base
# 최상단의 database.py에서 Base를 가져옵니다.
from database import Base

class TeamInfoB(Base):
    __tablename__ = 'team_info_b'
    __table_args__ = {'comment': '팀정보 기본'}

    team_uid = Column(String(50), primary_key=True, comment='팀아이디')
    teamname = Column(String(100), comment='팀명')
    region_cd = Column(String(20), comment='지역')
    location = Column(String(255), comment='위치')
    start_time = Column(String(10), comment='활동시간FR')
    end_time = Column(String(10), comment='활동시간TO')
    day_cd = Column(String(20), comment='활동요일')
    level_cd = Column(String(10), comment='실력 (01: S, 02: A, 03: B, 04: C, 05: D, 06: F)')
    gender_cd = Column(String(10), comment='성별 (01:남자, 02: 여자, 03: 혼성)')
    use_yn = Column(String(1), comment='사용여부')
    comment = Column(String(255), comment='코멘트')
    create_id = Column(String(50), comment='등록자')
    create_dt = Column(DateTime, comment='등록시간')
    update_id = Column(String(50), comment='수정자')
    update_dt = Column(DateTime, comment='수정시간')