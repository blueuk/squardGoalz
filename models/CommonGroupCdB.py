from sqlalchemy import Column, String, Integer, DateTime, Numeric
from sqlalchemy.orm import declarative_base
# 최상단의 database.py에서 Base를 가져옵니다.
from database import Base

class CommonGroupCdB(Base):
    __tablename__ = 'common_group_cd_b'
    __table_args__ = {'comment': '공통코드그룹'}

    group_cd = Column(String(20), primary_key=True, comment='그룹코드')
    group_name = Column(String(100), comment='그룹코드명')
    use_yn = Column(String(1), comment='사용유무')
    start_date = Column(String(8), comment='적용시작일자')
    end_date = Column(String(8), comment='적용종료일자')
    create_id = Column(String(50), comment='등록자')
    create_dt = Column(DateTime, comment='등록시간')
    update_id = Column(String(50), comment='수정자')
    update_dt = Column(DateTime, comment='수정시간')