from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from models.CommonCdB import CommonCdB
from models.CommonGroupCdB import CommonGroupCdB
from common_cd import commonCdRequest

async def check_group_cd_exists(db: AsyncSession, group_cd: str) -> bool:
    if not group_cd:
        return False
    result = await db.execute(select(CommonGroupCdB).filter(CommonGroupCdB.group_cd == group_cd))
    return result.scalars().first() is not None

# ================== 그룹 코드(common_group_cd_b) 로직 ==================
async def get_group_codes(db: AsyncSession, req: commonCdRequest.CommonGroupCdSearchRequest):
    query = select(CommonGroupCdB)
    if req.group_cd:
        query = query.filter(CommonGroupCdB.group_cd.like(f"%{req.group_cd}%"))
    if req.group_name:
        query = query.filter(CommonGroupCdB.group_name.like(f"%{req.group_name}%"))
    if req.use_yn:
        query = query.filter(CommonGroupCdB.use_yn == req.use_yn)
        
    result = await db.execute(query)
    groups = result.scalars().all()
    
    if req.group_cd and not groups:
        raise ValueError("공통코드가 존재하지 않습니다.")
    return groups

async def insert_group_code(db: AsyncSession, req: commonCdRequest.CommonGroupCdInsertRequest, session_id: str):
    now = datetime.now()
    today_str = now.strftime("%Y%m%d")
    
    group_cd_obj = CommonGroupCdB(
        group_cd=req.group_cd,
        group_name=req.group_name,
        use_yn=req.use_yn,
        start_date=today_str,
        end_date="99991231",
        create_id=session_id,
        create_dt=now,
        update_id=session_id,
        update_dt=now
    )
    db.add(group_cd_obj)
    await db.commit()
    return group_cd_obj

async def update_group_code(db: AsyncSession, req: commonCdRequest.CommonGroupCdUpdateRequest, session_id: str):
    result = await db.execute(select(CommonGroupCdB).filter(CommonGroupCdB.group_cd == req.group_cd))
    obj = result.scalars().first()
    if not obj:
        raise ValueError("공통코드가 존재하지 않습니다.")
        
    if req.group_name is not None:
        obj.group_name = req.group_name
    if req.use_yn is not None:
        obj.use_yn = req.use_yn
    if req.end_date is not None:
        obj.end_date = req.end_date
        
    obj.update_id = session_id
    obj.update_dt = datetime.now()
    
    await db.commit()
    return obj

# ================== 상세 코드(common_cd_b) 로직 ==================
async def get_common_codes(db: AsyncSession, req: commonCdRequest.CommonCdSearchRequest):
    # 1. 그룹코드 존재 여부 검증
    if req.group_cd:
        exists = await check_group_cd_exists(db, req.group_cd)
        if not exists:
            raise ValueError("공통코드가 존재하지 않습니다.")
            
    query = select(CommonCdB)
    if req.group_cd:
        query = query.filter(CommonCdB.group_cd == req.group_cd)
    if req.code:
        query = query.filter(CommonCdB.code.like(f"%{req.code}%"))
    if req.use_yn:
        query = query.filter(CommonCdB.use_yn == req.use_yn)
        
    query = query.order_by(CommonCdB.code_seq.asc())
    
    result = await db.execute(query)
    return result.scalars().all()

async def insert_common_code(db: AsyncSession, req: commonCdRequest.CommonCdInsertRequest, session_id: str):
    # 1. 그룹코드 존재 여부 검증
    exists = await check_group_cd_exists(db, req.group_cd)
    if not exists:
        raise ValueError("공통코드가 존재하지 않습니다.")
        
    now = datetime.now()
    
    cd_obj = CommonCdB(
        group_cd=req.group_cd,
        code=req.code,
        code_name=req.code_name,
        code_seq=req.code_seq,
        reference_1=req.reference_1,
        reference_2=req.reference_2,
        reference_3=req.reference_3,
        reference_4=req.reference_4,
        use_yn=req.use_yn,
        create_id=session_id,
        create_dt=now,
        update_id=session_id,
        update_dt=now
    )
    db.add(cd_obj)
    await db.commit()
    return cd_obj

async def update_common_code(db: AsyncSession, req: commonCdRequest.CommonCdUpdateRequest, session_id: str):
    result = await db.execute(select(CommonCdB).filter(CommonCdB.group_cd == req.group_cd, CommonCdB.code == req.code))
    obj = result.scalars().first()
    if not obj:
        raise ValueError("공통코드가 존재하지 않습니다.")
        
    if req.code_name is not None: obj.code_name = req.code_name
    if req.code_seq is not None: obj.code_seq = req.code_seq
    if req.reference_1 is not None: obj.reference_1 = req.reference_1
    if req.reference_2 is not None: obj.reference_2 = req.reference_2
    if req.reference_3 is not None: obj.reference_3 = req.reference_3
    if req.reference_4 is not None: obj.reference_4 = req.reference_4
    if req.use_yn is not None: obj.use_yn = req.use_yn
    
    obj.update_id = session_id
    obj.update_dt = datetime.now()
    
    await db.commit()
    return obj

