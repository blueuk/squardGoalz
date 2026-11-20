import re
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.TeamMemberL import TeamMemberL
from models.TeamMemberMbtiL import TeamMemberMbtiL
from memberMbti import memberMbtiRequest

# 테스트 종류별 유형 코드 형식, 축 순서, 문항 수
CODE_PATTERN = {'field': r'^[FB][WC][PT][SL]$', 'gk': r'^G-[PT][SL]$'}
AXES = {'field': ['fb_pct', 'cw_pct', 'pt_pct', 'sl_pct'], 'gk': ['pt_pct', 'sl_pct']}
QUESTION_COUNT = {'field': 32, 'gk': 16}
# 축별 글자: 성향 %가 50 초과면 앞 글자, 50 미만이면 뒤 글자 (정확히 50이면 어느 쪽이든 허용)
LETTERS = {'fb_pct': 'FB', 'cw_pct': 'WC', 'pt_pct': 'PT', 'sl_pct': 'SL'}

async def get(db: AsyncSession, req: memberMbtiRequest.MemberMbtiSearchRequest):
    query = select(TeamMemberMbtiL).filter(TeamMemberMbtiL.team_uid == req.team_uid)
    if req.member_uid:
        query = query.filter(TeamMemberMbtiL.member_uid == req.member_uid)
    return (await db.execute(query)).scalars().all()

def _validate(req: memberMbtiRequest.MemberMbtiSaveRequest):
    if not re.match(CODE_PATTERN[req.test_type], req.mbti_cd):
        raise ValueError("유형 코드 형식이 올바르지 않습니다.")
    if not re.fullmatch(r'[1-5]+', req.answers) or len(req.answers) != QUESTION_COUNT[req.test_type]:
        raise ValueError("응답이 올바르지 않습니다.")
    letters = req.mbti_cd.replace('G-', '')
    for letter, axis in zip(letters, AXES[req.test_type]):
        pct = getattr(req, axis)
        if pct is None:
            raise ValueError("성향 비율이 비어 있습니다.")
        expected = LETTERS[axis][0] if pct > 50 else LETTERS[axis][1] if pct < 50 else letter
        if letter != expected:
            raise ValueError("유형 코드와 성향 비율이 맞지 않습니다.")

async def save(db: AsyncSession, req: memberMbtiRequest.MemberMbtiSaveRequest, session_id: str):
    """멤버의 테스트 종류별 결과를 저장 (다시 테스트하면 덮어씀)"""
    _validate(req)
    member = (await db.execute(select(TeamMemberL).filter(
        TeamMemberL.team_uid == req.team_uid,
        TeamMemberL.member_uid == req.member_uid,
        TeamMemberL.terminate_dt.is_(None),
    ))).scalars().first()
    if not member:
        raise ValueError("선수 명단에 없는 멤버입니다.")

    now = datetime.now()
    obj = await db.get(TeamMemberMbtiL, (req.team_uid, req.member_uid, req.test_type))
    if not obj:
        obj = TeamMemberMbtiL(
            team_uid=req.team_uid, member_uid=req.member_uid, test_type=req.test_type,
            create_id=session_id, create_dt=now,
        )
        db.add(obj)
    obj.mbti_cd = req.mbti_cd
    # 골레이 테스트에는 전방/후방, 중앙/측면 축이 없음
    obj.fb_pct = req.fb_pct if req.test_type == 'field' else None
    obj.cw_pct = req.cw_pct if req.test_type == 'field' else None
    obj.pt_pct = req.pt_pct
    obj.sl_pct = req.sl_pct
    obj.answers = req.answers
    obj.question_ver = req.question_ver
    obj.update_id = session_id
    obj.update_dt = now
    await db.commit()
