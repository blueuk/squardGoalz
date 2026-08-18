from sqlalchemy import Column, String, Integer, DateTime, Numeric
from sqlalchemy.orm import declarative_base
# 최상단의 database.py에서 Base를 가져옵니다.
from database import Base

class UserB(Base):
    __tablename__ = 'user_b'
    __table_args__ = {'comment': '유저정보 기본'}

    userid = Column(String(50), primary_key=True, comment='아이디')
    username = Column(String(50), comment='이름')
    ip = Column(String(50), comment='IP')
    last_login_dt = Column(DateTime, comment='최종접속일자')
    use_yn = Column(String(1), comment='사용여부 (Y/N)')
    nickname = Column(String(50), comment='닉네임')
    kakao_name = Column(String(100), comment='카카오닉네임')
    auth_cd = Column(String(10), comment='권한코드 (01:관리자, 02:일반)')
    phone = Column(String(20), comment='전화번호')
    create_dt = Column(DateTime, comment='등록일자')
    update_dt = Column(DateTime, comment='수정일자')