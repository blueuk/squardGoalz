from sqlalchemy import Column, String, Integer, DateTime, Numeric
from sqlalchemy.orm import declarative_base
# 최상단의 database.py에서 Base를 가져옵니다.
from database import Base

class UserH(Base):
    __tablename__ = 'user_h'
    __table_args__ = {'comment': '유저정보 이력'}

    userid = Column(String(50), primary_key=True, comment='아이디')
    user_seq = Column(Numeric, primary_key=True, comment='시퀀스')
    username = Column(String(50), comment='이름')
    use_yn = Column(String(1), comment='사용여부')
    nickname = Column(String(50), comment='닉네임')
    kakao_name = Column(String(100), comment='카카오닉네임')
    auth_cd = Column(String(10), comment='권한코드 (01:관리자, 02:일반)')
    phone = Column(String(20), comment='전화번호')
    create_dt = Column(DateTime, comment='등록일자')
    update_dt = Column(DateTime, comment='수정일자')