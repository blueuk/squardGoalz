from sqlalchemy import Column, String, Integer, DateTime
# 최상단의 database.py에서 Base를 가져옵니다.
from database import Base

class TeamMemberMbtiL(Base):
    __tablename__ = 'team_member_mbti_l'
    __table_args__ = {'comment': '팀 멤버 풋살 MBTI 결과 리스트'}

    team_uid = Column(String(50), primary_key=True, comment='팀아이디')
    member_uid = Column(String(50), primary_key=True, comment='멤버아이디')
    test_type = Column(String(10), primary_key=True, comment='테스트 종류 (field: 필드, gk: 골레이)')
    mbti_cd = Column(String(10), comment='유형 코드 (필드 예: FCPL, 골레이 예: G-PS)')
    fb_pct = Column(Integer, comment='F 전방 성향 % (100-값 = B 후방, 골레이는 없음)')
    cw_pct = Column(Integer, comment='W 측면 성향 % (100-값 = C 중앙, 골레이는 없음)')
    pt_pct = Column(Integer, comment='P 파워 성향 % (100-값 = T 테크닉)')
    sl_pct = Column(Integer, comment='S 해결 성향 % (100-값 = L 연결)')
    answers = Column(String(100), comment='문항 번호 순 응답 (1~5), 문항이 바뀌어도 다시 계산할 수 있게 보관')
    question_ver = Column(String(10), comment='문항 버전')
    create_id = Column(String(50), comment='등록자')
    create_dt = Column(DateTime, comment='등록시간')
    update_id = Column(String(50), comment='수정자')
    update_dt = Column(DateTime, comment='수정시간')
