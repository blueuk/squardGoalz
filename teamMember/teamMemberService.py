from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, or_
from datetime import datetime
import uuid
from models.TeamMemberL import TeamMemberL
from models.CommonCdB import CommonCdB
from models.TeamMemberScoreL import TeamMemberScoreL
from models.TeamInfoB import TeamInfoB
from models.TeamVoteL import TeamVoteL
from models.TeamRecordL import TeamRecordL
from models.UserB import UserB
from models.UserH import UserH
from user import userService
from user.userRequest import UserUpdateRequest
from teamMember import teamMemberRequest

async def _search_members(db: AsyncSession, req: teamMemberRequest.TeamMemberSearchRequest, terminated: bool):
    # TeamMemberL과 TeamInfoB를 Join하여 팀명을 함께 가져옵니다.
    query = select(TeamMemberL, TeamInfoB.teamname).outerjoin(
        TeamInfoB, TeamMemberL.team_uid == TeamInfoB.team_uid
    )
    
    # terminate_dt 유무로 선수단 / 탈퇴자 목록을 구분합니다.
    if terminated:
        query = query.filter(TeamMemberL.terminate_dt.isnot(None))
    else:
        query = query.filter(TeamMemberL.terminate_dt.is_(None))
    
    if req.team_uid:
        query = query.filter(TeamMemberL.team_uid == req.team_uid)
    if req.teamname:
        query = query.filter(TeamInfoB.teamname.like(f"%{req.teamname}%"))
    if req.member_name:
        query = query.filter(TeamMemberL.member_name.like(f"%{req.member_name}%"))
        
    result = await db.execute(query)
    
    response_list = []
    for member_obj, teamname in result.all():
        resp = member_obj.__dict__.copy()
        resp['teamname'] = teamname
        response_list.append(resp)
        
    return response_list

async def get_team_members(db: AsyncSession, req: teamMemberRequest.TeamMemberSearchRequest):
    return await _search_members(db, req, terminated=False)

async def get_terminated_members(db: AsyncSession, req: teamMemberRequest.TeamMemberSearchRequest):
    return await _search_members(db, req, terminated=True)

def add_new_member(db: AsyncSession, team_uid: str, member_name: str, user_id, gender_cd, status_cd,
                   score_cds, session_id: str, now: datetime) -> str:
    """신규 멤버 + 모든 score_cd 기본 점수(13점, 올해) 추가. commit은 호출하는 쪽에서 함"""
    new_member_uid = str(uuid.uuid4())
    db.add(TeamMemberL(
        team_uid=team_uid,
        member_uid=new_member_uid,
        member_name=member_name,
        user_id=user_id,
        sign_dt=now.strftime("%Y%m%d%H%M%S"),  # 14자리 YYYYMMDDHHMMSS
        gender_cd=gender_cd,
        status_cd=status_cd,
        create_id=session_id,
        create_dt=now
    ))
    for sc in score_cds:
        db.add(TeamMemberScoreL(
            member_uid=new_member_uid,
            team_uid=team_uid,
            year=str(now.year),
            score_cd=sc.code,
            score_val=13,
            create_id=session_id,
            create_dt=now,
            update_id=session_id,
            update_dt=now
        ))
    return new_member_uid

async def get_score_cds(db: AsyncSession):
    return (await db.execute(select(CommonCdB).where(CommonCdB.group_cd == 'score_cd'))).scalars().all()

async def insert_team_members(db: AsyncSession, req: teamMemberRequest.TeamMemberInsertRequest, session_id: str):
    now = datetime.now()
    score_cds = await get_score_cds(db)

    for member in req.members:
        add_new_member(db, member.team_uid, member.member_name, member.user_id,
                       member.gender_cd, member.status_cd, score_cds, session_id, now)

    await db.commit()

async def update_team_member(db: AsyncSession, req: teamMemberRequest.TeamMemberUpdateRequest):
    result = await db.execute(
        select(TeamMemberL).filter(
            TeamMemberL.team_uid == req.team_uid,
            TeamMemberL.member_uid == req.member_uid
        )
    )
    obj = result.scalars().first()
    
    if not obj:
        raise ValueError("업데이트할 멤버가 존재하지 않습니다.")
        
    if req.member_name is not None: obj.member_name = req.member_name
    if req.user_id is not None: obj.user_id = req.user_id
    if req.gender_cd is not None: obj.gender_cd = req.gender_cd
    if req.status_cd is not None: obj.status_cd = req.status_cd
    
    await db.commit()
    return obj

async def terminate_team_member(db: AsyncSession, req: teamMemberRequest.TeamMemberTerminateRequest):
    result = await db.execute(
        select(TeamMemberL).filter(
            TeamMemberL.team_uid == req.team_uid,
            TeamMemberL.member_uid == req.member_uid
        )
    )
    obj = result.scalars().first()
    
    if not obj:
        raise ValueError("탈퇴 처리할 멤버가 존재하지 않습니다.")
    if obj.terminate_dt:
        raise ValueError("이미 탈퇴 처리된 멤버입니다.")
        
    now_str = datetime.now().strftime("%Y%m%d%H%M%S")
    obj.terminate_dt = now_str
    
    await db.commit()
    return obj

async def _get_terminated_member(db: AsyncSession, team_uid: str, member_uid: str):
    result = await db.execute(
        select(TeamMemberL).filter(
            TeamMemberL.team_uid == team_uid,
            TeamMemberL.member_uid == member_uid,
            TeamMemberL.terminate_dt.isnot(None)
        )
    )
    obj = result.scalars().first()
    
    if not obj:
        raise ValueError("탈퇴자 목록에 해당 멤버가 존재하지 않습니다.")
    return obj

async def restore_team_member(db: AsyncSession, req: teamMemberRequest.TeamMemberRestoreRequest):
    obj = await _get_terminated_member(db, req.team_uid, req.member_uid)
    obj.terminate_dt = None
    
    await db.commit()
    return obj

async def delete_team_member(db: AsyncSession, req: teamMemberRequest.TeamMemberDeleteRequest):
    obj = await _get_terminated_member(db, req.team_uid, req.member_uid)
    
    # 멤버에 연결된 점수 / 투표 / 기록 데이터까지 완전 삭제합니다.
    await db.execute(delete(TeamMemberScoreL).where(
        TeamMemberScoreL.team_uid == req.team_uid,
        TeamMemberScoreL.member_uid == req.member_uid
    ))
    await db.execute(delete(TeamVoteL).where(
        TeamVoteL.team_uid == req.team_uid,
        TeamVoteL.member_uid == req.member_uid
    ))
    await db.execute(delete(TeamRecordL).where(
        TeamRecordL.team_uid == req.team_uid,
        TeamRecordL.member_uid == req.member_uid
    ))
    await db.delete(obj)
    
    await db.commit()


# ── 가입 승인 ──────────────────────────────────────────────────────────────
# 선수 명단(탈퇴하지 않은 멤버)에 연결되지 않은 일반 회원 = 승인 대기

def _active_linked_user_ids(team_uid: str):
    return select(TeamMemberL.user_id).where(
        TeamMemberL.team_uid == team_uid,
        TeamMemberL.terminate_dt.is_(None),
        TeamMemberL.user_id.isnot(None)
    )

async def get_pending_users(db: AsyncSession, team_uid: str):
    from auth import ADMIN_AUTH_CD
    result = await db.execute(
        select(UserB).where(
            or_(UserB.auth_cd.is_(None), UserB.auth_cd != ADMIN_AUTH_CD),
            or_(UserB.use_yn.is_(None), UserB.use_yn == 'Y'),
            UserB.userid.notin_(_active_linked_user_ids(team_uid))
        ).order_by(UserB.create_dt)
    )
    return result.scalars().all()

async def _get_pending_user(db: AsyncSession, team_uid: str, userid: str) -> UserB:
    pending = {u.userid: u for u in await get_pending_users(db, team_uid)}
    if userid not in pending:
        raise ValueError("승인 대기 중인 회원이 아닙니다.")
    return pending[userid]

async def approve_user(db: AsyncSession, req: teamMemberRequest.TeamMemberApproveRequest, session_id: str):
    """기존 선수(member_uid)에 연결하거나, 없으면 신규 선수로 등록"""
    user = await _get_pending_user(db, req.team_uid, req.userid)

    if req.member_uid:
        member = (await db.execute(select(TeamMemberL).where(
            TeamMemberL.team_uid == req.team_uid,
            TeamMemberL.member_uid == req.member_uid,
            TeamMemberL.terminate_dt.is_(None)
        ))).scalars().first()
        if not member:
            raise ValueError("연결할 선수가 선수 명단에 없습니다.")
        if member.user_id:
            raise ValueError("이미 다른 계정이 연결된 선수입니다.")
        member.user_id = user.userid
        # 가입 시 이름을 잘못 입력했을 수 있으므로 계정 이름을 명단 이름으로 맞춤 (이력 적재 + 연결과 함께 commit)
        await userService.update_user(db, UserUpdateRequest(userid=user.userid, username=member.member_name))
        return
    else:
        add_new_member(db, req.team_uid, user.username or user.nickname or user.userid, user.userid,
                       '01', '01', await get_score_cds(db), session_id, datetime.now())

    await db.commit()

async def reject_user(db: AsyncSession, req: teamMemberRequest.TeamMemberRejectRequest):
    """승인 대기 회원의 계정을 삭제 (다시 카카오 로그인하면 가입 화면부터 다시 진행)"""
    await _get_pending_user(db, req.team_uid, req.userid)
    # 탈퇴 처리된 선수에 남아 있는 연결도 해제
    await db.execute(update(TeamMemberL).where(TeamMemberL.user_id == req.userid).values(user_id=None))
    await db.execute(delete(UserH).where(UserH.userid == req.userid))
    await db.execute(delete(UserB).where(UserB.userid == req.userid))
    await db.commit()
