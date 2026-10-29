"""화면별 기능 권한 목록

- 버튼/API 가 코드에 있으므로 권한 목록도 코드에서 관리하고,
  역할(auth_cd)별 부여 여부만 auth_role_permission_l 에 저장합니다.
- 관리자(01)는 항상 전체 권한을 가지며, 권한 설정(auth.manage)은 관리자 전용입니다.
"""

PERMISSIONS = [
    # (권한코드, 화면, 권한명, 설명)
    ('arrange.manage',    '홈',     '팀 배정',          '배정하기, 다시 배정, 배정 저장'),
    ('schedule.manage',   '일정',   '일정 관리',        '일정 등록, 시간/장소 수정, 일정 삭제'),
    ('vote.manage',       '일정',   '투표 관리',        '다른 팀원 투표 상태 변경, 미투표 일괄 초기화, 경기취소'),
    ('schedule.past',     '일정',   '지난 일정 수정',   '오늘 이전 날짜의 일정/투표 수정'),
    ('team.edit',         '팀관리', '팀 정보 수정',     '팀 기본 정보 수정'),
    ('payment.edit',      '팀관리', '입금 안내 수정',   '입금 항목/금액/계좌 수정'),
    ('weight.manage',     '팀관리', '포지션 가중치 관리', '가중치 수정, 능력치 항목 추가/삭제'),
    ('member.manage',     '선수단', '선수 관리',        '선수 추가, 상태 변경, 탈퇴 처리'),
    ('member.terminated', '선수단', '탈퇴자 관리',      '탈퇴자 목록 조회, 복구, 완전 삭제'),
    ('score.view',        '선수단', '능력치 상세 보기', '능력치 수치/평균 보기'),
    ('score.edit',        '선수단', '능력치 수정',      '선수 능력치 점수 수정'),
]

# 관리자 전용 (역할에 부여할 수 없음)
ADMIN_ONLY_PERMISSIONS = ['auth.manage']

GRANTABLE_CODES = {p[0] for p in PERMISSIONS}
ALL_CODES = [p[0] for p in PERMISSIONS] + ADMIN_ONLY_PERMISSIONS
