from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime
import uuid
from models.TeamMemberL import TeamMemberL
from models.TeamInfoB import TeamInfoB
from teamMember import teamMemberRequest

async def get_team_members(db: AsyncSession, req: teamMemberRequest.TeamMemberSearchRequest):
    # TeamMemberL과 TeamInfoB를 Join하여 팀명을 함께 가져옵니다.
    query = select(TeamMemberL, TeamInfoB.teamname).outerjoin(
        TeamInfoB, TeamMemberL.team_uid == TeamInfoB.team_uid
    )
    
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

async def insert_team_members(db: AsyncSession, req: teamMemberRequest.TeamMemberInsertRequest, session_id: str):
    now = datetime.now()
    sign_date_str = now.strftime("%Y%m%d%H%M%S") # 14자리 YYYYMMDDHHMMSS
    
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
        
    now_str = datetime.now().strftime("%Y%m%d%H%M%S")
    obj.terminate_dt = now_str
    
    await db.commit()
    return obj

