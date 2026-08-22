from sqlalchemy.ext.asyncio import AsyncSession
from user import userService
from user.userRequest import UserUpdateRequest
from datetime import datetime

async def process_login(db: AsyncSession, userid: str, ip: str) -> bool:
    """유저가 존재하는지 확인하고, 존재하면 IP와 최근 로그인 일시를 업데이트합니다."""
    users = await userService.get_users(db, userid=userid)
    
    if not users:
        # 가입된 계정이 없음
        return False
        
    # 계정이 있으면 로그인 처리 (최종 접속일, IP 업데이트)
    update_req = UserUpdateRequest(
        userid=userid,
        ip=ip,
        last_login_dt=datetime.now()
    )
    await userService.update_user(db, update_req)
    return True

