from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from auth import get_session_userid, require_self_or_permission
from memberProfile import memberProfileService

router = APIRouter(prefix='/profile', tags=['MemberProfile'])

class ProfileVersionResponse(BaseModel):
    member_uid: str
    version: str  # 이미지 주소의 v 값

class ProfileDeleteRequest(BaseModel):
    team_uid: str
    member_uid: str

class ProfileSaveResponse(BaseModel):
    message: str
    version: Optional[str] = None

@router.get('/search', response_model=List[ProfileVersionResponse])
async def search(team_uid: str, request: Request, member_uid: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    """[로그인] 프로필 사진이 있는 멤버와 버전을 조회합니다 (이미지 본문 제외)."""
    get_session_userid(request)
    return await memberProfileService.get_versions(db, team_uid, member_uid)

@router.get('/image/{team_uid}/{member_uid}')
async def image(team_uid: str, member_uid: str, request: Request, db: AsyncSession = Depends(get_db)):
    """[로그인] 프로필 사진. 주소에 버전(v)이 붙으므로 브라우저가 오래 저장해도 됨"""
    get_session_userid(request)
    obj = await memberProfileService.get_image(db, team_uid, member_uid)
    if not obj:
        raise HTTPException(status_code=404, detail="프로필 사진이 없습니다.")
    return Response(
        content=obj.image,
        media_type=obj.content_type,
        headers={'Cache-Control': 'private, max-age=31536000, immutable'},
    )

@router.post('/upload', response_model=ProfileSaveResponse)
async def upload(
    request: Request,
    team_uid: str = Form(...),
    member_uid: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """[본인 또는 권한: member.manage] 프로필 사진을 저장합니다 (최대 100KB, 바꾸면 덮어씀)."""
    userid = await require_self_or_permission(request, db, team_uid, member_uid, 'member.manage')
    data = await file.read(memberProfileService.MAX_IMAGE_BYTES + 1)
    try:
        version = await memberProfileService.save(db, team_uid, member_uid, data, userid)
        return ProfileSaveResponse(message='프로필 사진 저장 완료', version=version)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/delete', response_model=ProfileSaveResponse)
async def delete(req: ProfileDeleteRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """[본인 또는 권한: member.manage] 프로필 사진을 삭제합니다."""
    await require_self_or_permission(request, db, req.team_uid, req.member_uid, 'member.manage')
    await memberProfileService.delete_image(db, req.team_uid, req.member_uid)
    return ProfileSaveResponse(message='프로필 사진 삭제 완료')
