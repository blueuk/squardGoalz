from sqlalchemy import Column, String, DateTime
# 최상단의 database.py에서 Base를 가져옵니다.
from database import Base

class AuthRolePermissionL(Base):
    __tablename__ = 'auth_role_permission_l'
    __table_args__ = {'comment': '역할별 기능 권한 리스트'}

    auth_cd = Column(String(10), primary_key=True, comment='권한코드 (common_cd auth_cd)')
    perm_cd = Column(String(50), primary_key=True, comment='기능권한코드 (permissionCatalog)')
    create_id = Column(String(50), comment='등록자')
    create_dt = Column(DateTime, comment='등록시간')
