from sqlalchemy import Column, String, Integer, DateTime, Numeric
from sqlalchemy.orm import declarative_base
# 최상단의 database.py에서 Base를 가져옵니다.
from database import Base

class CommonCdB(Base):
    __tablename__ = 'common_cd_b'
    __table_args__ = {'comment': '공통코드'}

    group_cd = Column(String(20), primary_key=True, comment='그룹코드')
    code = Column(String(20), primary_key=True, comment='코드')
    code_name = Column(String(100), comment='코드명')
    code_seq = Column(Integer, comment='코드순서')
    reference_1 = Column(String(255), comment='참조1')
    reference_2 = Column(String(255), comment='참조2')
    reference_3 = Column(String(255), comment='참조3')
    reference_4 = Column(String(255), comment='참조4')
    use_yn = Column(String(1), comment='사용유무')
    create_id = Column(String(50), comment='등록자')
    create_dt = Column(DateTime, comment='등록시간')
    update_id = Column(String(50), comment='수정자')
    update_dt = Column(DateTime, comment='수정시간')