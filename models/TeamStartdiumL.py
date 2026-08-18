from sqlalchemy import Column, String, Integer, DateTime, Numeric
from sqlalchemy.orm import declarative_base
# 최상단의 database.py에서 Base를 가져옵니다.
from database import Base

class TeamStartdiumL(Base):
    __tablename__ = 'team_startdium_l'
    __table_args__ = {'comment': '팀 구장 리스트'}

    team_uid = Column(String(50), primary_key=True, comment='팀아이디')
    team_stardium_seq = Column(Integer, primary_key=True, autoincrement=True, comment='시퀀스')
    location = Column(String(255), comment='위치')
    start_time = Column(String(10), comment='활동시간FR')
    end_time = Column(String(10), comment='활동시간TO')
    day_cd = Column(String(20), comment='활동요일')
    main_locate_yn = Column(String(1), comment='주구장여부')
    create_id = Column(String(50), comment='등록자')
    create_dt = Column(DateTime, comment='등록시간')
    update_id = Column(String(50), comment='수정자')
    update_dt = Column(DateTime, comment='수정시간')