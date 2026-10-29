from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_db
from auth import require_permission, require_self_or_permission
from teamMember.teamMemberRequest import (
    TeamMemberSearchRequest, TeamMemberInsertRequest,
    TeamMemberUpdateRequest, TeamMemberTerminateRequest,
    TeamMemberRestoreRequest, TeamMemberDeleteRequest
)
from teamMember.teamMemberResponse import TeamMemberResponse, MessageResponse
from teamMember import teamMemberService

router = APIRouter(prefix="/team_member", tags=["TeamMember"])

@router.get("/search", response_model=List[TeamMemberResponse])
async def search_team_members(req: TeamMemberSearchRequest = Depends(), db: AsyncSession = Depends(get_db)):
    """GET 방식으로 team_info_b와 조인하여 멤버를 검색합니다 (teamname, member_name LIKE)."""
    try:
        return await teamMemberService.get_team_members(db, req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/insert", response_model=MessageResponse)
async def insert_team_members(req: TeamMemberInsertRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """POST 방식으로 멤버 정보를 리스트 형태로 대량(Bulk) Insert 합니다."""
    userid = await require_permission(request, db, 'member.manage')
    try:
        await teamMemberService.insert_team_members(db, req, userid)
        return MessageResponse(message=f"{len(req.members)}명의 멤버가 등록되었습니다.")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update", response_model=MessageResponse)
async def update_team_member(req: TeamMemberUpdateRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """POST 방식으로 개별 멤버의 정보를 수정합니다."""
    await require_self_or_permission(request, db, req.team_uid, req.member_uid, 'member.manage')
    try:
        await teamMemberService.update_team_member(db, req)
        return MessageResponse(message="멤버 정보 수정 완료")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/terminate", response_model=MessageResponse)
async def terminate_team_member(req: TeamMemberTerminateRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """POST 방식으로 멤버의 탈퇴일자(terminate_dt)를 기록합니다."""
    await require_permission(request, db, 'member.manage')
    try:
        await teamMemberService.terminate_team_member(db, req)
        return MessageResponse(message="멤버 탈퇴(종료) 처리 완료")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/terminated/search", response_model=List[TeamMemberResponse])
async def search_terminated_members(request: Request, req: TeamMemberSearchRequest = Depends(), db: AsyncSession = Depends(get_db)):
    """[권한: member.terminated] GET 방식으로 탈퇴자 목록을 검색합니다 (teamname, member_name LIKE)."""
    await require_permission(request, db, 'member.terminated')
    try:
        return await teamMemberService.get_terminated_members(db, req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/restore", response_model=MessageResponse)
async def restore_team_member(req: TeamMemberRestoreRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """[권한: member.terminated] POST 방식으로 탈퇴자를 선수단 목록으로 복구합니다."""
    await require_permission(request, db, 'member.terminated')
    try:
        await teamMemberService.restore_team_member(db, req)
        return MessageResponse(message="멤버 복구 완료")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/delete", response_model=MessageResponse)
async def delete_team_member(req: TeamMemberDeleteRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """[권한: member.terminated] POST 방식으로 탈퇴자를 완전 삭제합니다 (점수/투표/기록 포함)."""
    await require_permission(request, db, 'member.terminated')
    try:
        await teamMemberService.delete_team_member(db, req)
        return MessageResponse(message="멤버 완전 삭제 완료")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
