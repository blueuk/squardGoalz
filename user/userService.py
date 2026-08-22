from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from datetime import datetime
from models.UserB import UserB
from models.UserH import UserH
from user.userRequest import UserInsertRequest, UserUpdateRequest

async def get_next_seq(db: AsyncSession, userid: str) -> int:
    """UserH 테이블의 user_seq 채번 함수"""
    result = await db.execute(select(func.max(UserH.user_seq)).filter(UserH.userid == userid))
    max_seq = result.scalar()
    return int(max_seq + 1) if max_seq else 1

async def insert_user(db: AsyncSession, req: UserInsertRequest):
    now = datetime.now()
    
    # 1. USER_B (유저 기본정보) 등록
    user_b = UserB(
        userid=req.userid,
        username=req.username,
        nickname=req.nickname,
        auth_cd=req.auth_cd,
        phone=req.phone,
        create_dt=now,
        update_dt=now,
        use_yn='Y'
    )
    db.add(user_b)
    
    # 2. USER_H (유저 이력) 등록
    seq = await get_next_seq(db, req.userid)
    user_h = UserH(
        userid=req.userid,
        user_seq=seq,
        username=req.username,
        nickname=req.nickname,
        auth_cd=req.auth_cd,
        phone=req.phone,
        create_dt=now,
        update_dt=now,
        use_yn='Y'
    )
    db.add(user_h)
    
    await db.commit()
    return user_b

async def get_users(db: AsyncSession, userid: str = None, username: str = None, nickname: str = None, phone: str = None):
    query = select(UserB)
    if userid:
        query = query.filter(UserB.userid == userid)
    if username:
        query = query.filter(UserB.username.like(f"%{username}%"))
    if nickname:
        query = query.filter(UserB.nickname.like(f"%{nickname}%"))
    if phone:
        query = query.filter(UserB.phone == phone)
        
    result = await db.execute(query)
    return result.scalars().all()

async def update_user(db: AsyncSession, req: UserUpdateRequest):
    now = req.update_dt or datetime.now()
    
    # 1. USER_B 조회
    result = await db.execute(select(UserB).filter(UserB.userid == req.userid))
    user_b = result.scalars().first()
    if not user_b:
        return None
        
    # 이력(UserH) 적재가 필요한 항목이 변경되었는지 체크할 변수
    needs_history = False
        
    # 2. 파라미터로 넘어온 필드 업데이트
    # ip, last_login_dt는 값이 들어와도 이력 적재 플래그(needs_history)를 켜지 않음
    if req.ip is not None:
        user_b.ip = req.ip
    if req.last_login_dt is not None:
        user_b.last_login_dt = req.last_login_dt
        
    # 그 외 주요 정보들(권한, 닉네임 등)이 기존과 다르게 변경되었을 때만 플래그 ON
    if req.use_yn is not None and user_b.use_yn != req.use_yn:
        user_b.use_yn = req.use_yn
        needs_history = True
    if req.nickname is not None and user_b.nickname != req.nickname:
        user_b.nickname = req.nickname
        needs_history = True
    if req.kakao_name is not None and user_b.kakao_name != req.kakao_name:
        user_b.kakao_name = req.kakao_name
        needs_history = True
    if req.auth_cd is not None and user_b.auth_cd != req.auth_cd:
        user_b.auth_cd = req.auth_cd
        needs_history = True
    if req.phone is not None and user_b.phone != req.phone:
        user_b.phone = req.phone
        needs_history = True
        
    user_b.update_dt = now

    # 3. 중요 정보가 변경된 경우에만 USER_H에 이력 추가 삽입
    if needs_history:
        seq = await get_next_seq(db, req.userid)
        user_h = UserH(
            userid=user_b.userid,
            user_seq=seq,
            username=user_b.username,
            nickname=user_b.nickname,
            kakao_name=user_b.kakao_name,
            auth_cd=user_b.auth_cd,
            phone=user_b.phone,
            use_yn=user_b.use_yn,
            create_dt=user_b.create_dt,  # 최초 등록일은 그대로
            update_dt=now                # 수정일은 현재(업데이트) 시간
        )
        db.add(user_h)
    
    await db.commit()
    return user_b

async def delete_user(db: AsyncSession, userid: str) -> bool:
    """UserB와 연결된 UserH 이력을 모두 삭제합니다."""
    # 1. 존재하는지 확인
    result = await db.execute(select(UserB).filter(UserB.userid == userid))
    user_b = result.scalars().first()
    
    if not user_b:
        return False
        
    # 2. USER_H 이력 삭제
    await db.execute(delete(UserH).where(UserH.userid == userid))
    
    # 3. USER_B 기본정보 삭제
    await db.execute(delete(UserB).where(UserB.userid == userid))
    
    await db.commit()
    return True
