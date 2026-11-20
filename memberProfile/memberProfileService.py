from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from models.TeamMemberL import TeamMemberL
from models.MemberProfileImageL import MemberProfileImageL

MAX_IMAGE_BYTES = 100 * 1024  # 브라우저에서 256x256으로 줄여 보내므로 보통 10~30KB

def detect_content_type(data: bytes) -> Optional[str]:
    """파일 앞부분으로 실제 이미지 형식 판별 (확장자·헤더만 믿지 않음)"""
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        return 'image/webp'
    if data[:3] == b'\xff\xd8\xff':
        return 'image/jpeg'
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        return 'image/png'
    return None

def version_of(obj: MemberProfileImageL) -> str:
    """이미지 주소에 붙일 버전 (바뀔 때만 브라우저가 다시 받도록)"""
    return (obj.update_dt or obj.create_dt or datetime.min).strftime('%Y%m%d%H%M%S%f')

async def get_versions(db: AsyncSession, team_uid: str, member_uid: Optional[str]):
    """사진이 있는 멤버와 버전 (이미지 본문은 제외)"""
    query = select(MemberProfileImageL.member_uid, MemberProfileImageL.create_dt, MemberProfileImageL.update_dt) \
        .filter(MemberProfileImageL.team_uid == team_uid)
    if member_uid:
        query = query.filter(MemberProfileImageL.member_uid == member_uid)
    rows = (await db.execute(query)).all()
    return [{"member_uid": r.member_uid, "version": version_of(r)} for r in rows]

async def get_image(db: AsyncSession, team_uid: str, member_uid: str) -> Optional[MemberProfileImageL]:
    return await db.get(MemberProfileImageL, (team_uid, member_uid))

async def save(db: AsyncSession, team_uid: str, member_uid: str, data: bytes, session_id: str) -> str:
    if not data:
        raise ValueError("사진이 비어 있습니다.")
    if len(data) > MAX_IMAGE_BYTES:
        raise ValueError("사진이 너무 큽니다. (최대 100KB)")
    content_type = detect_content_type(data)
    if not content_type:
        raise ValueError("WebP, JPEG, PNG 사진만 올릴 수 있습니다.")
    member = (await db.execute(select(TeamMemberL).filter(
        TeamMemberL.team_uid == team_uid,
        TeamMemberL.member_uid == member_uid,
        TeamMemberL.terminate_dt.is_(None),
    ))).scalars().first()
    if not member:
        raise ValueError("선수 명단에 없는 멤버입니다.")

    now = datetime.now()
    obj = await db.get(MemberProfileImageL, (team_uid, member_uid))
    if not obj:
        obj = MemberProfileImageL(team_uid=team_uid, member_uid=member_uid, create_id=session_id, create_dt=now)
        db.add(obj)
    obj.image = data
    obj.content_type = content_type
    obj.image_size = len(data)
    obj.update_id = session_id
    obj.update_dt = now
    await db.commit()
    return version_of(obj)

async def delete_image(db: AsyncSession, team_uid: str, member_uid: str):
    await db.execute(delete(MemberProfileImageL).where(
        MemberProfileImageL.team_uid == team_uid,
        MemberProfileImageL.member_uid == member_uid,
    ))
    await db.commit()
