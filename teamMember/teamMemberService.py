from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from datetime import datetime
import uuid
from models.TeamMemberL import TeamMemberL
from models.CommonCdB import CommonCdB
from models.TeamMemberScoreL import TeamMemberScoreL
from models.TeamInfoB import TeamInfoB
from models.TeamVoteL import TeamVoteL
from models.TeamRecordL import TeamRecordL
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

async def insert_team_members(db: AsyncSession, req: teamMemberRequest.TeamMemberInsertRequest, session_id: str):
    now = datetime.now()
    sign_date_str = now.strftime("%Y%m%d%H%M%S") # 14자리 YYYYMMDDHHMMSS
    
    # 스코어 코드 목록 미리 가져오기
    score_cds = (await db.execute(select(CommonCdB).where(CommonCdB.group_cd == 'score_cd'))).scalars().all()

    for member in req.members:
        # 멤버 고유 UID 발급
        new_member_uid = str(uuid.uuid4())
        
        obj = TeamMemberL(
            team_uid=member.team_uid,
            member_uid=new_member_uid,
            member_name=member.member_name,
            user_id=member.user_id,
            sign_dt=sign_date_str,
            gender_cd=member.gender_cd,
            status_cd=member.status_cd,
            create_id=session_id,
            create_dt=now
        )
        db.add(obj)
        
        # 신규 멤버에게 모든 score_cd에 대해 13점 기본값 부여
        for sc in score_cds:
            score_obj = TeamMemberScoreL(
                member_uid=new_member_uid,
                team_uid=member.team_uid,
                year='2026',
                score_cd=sc.code,
                score_val=13,
                create_id=session_id,
                create_dt=now,
                update_id=session_id,
                update_dt=now
            )
            db.add(score_obj)
            
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
