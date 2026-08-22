import os

modules = [
    {
        "folder": "teamAccount",
        "prefix": "teamAccount",
        "model": "TeamAccountL",
        "pks": ["team_uid", "team_account_seq", "bank_cd", "account_enc"],
        "auto_pks": ["team_account_seq"],
        "cols": ["team_uid", "team_account_seq", "bank_cd", "account_enc", "create_id", "create_dt", "update_id", "update_dt"]
    },
    {
        "folder": "teamArrange",
        "prefix": "teamArrange",
        "model": "TeamArrangeL",
        "pks": ["vote_uid"],
        "auto_pks": [],
        "cols": ["vote_uid", "play_date", "team_cd", "member_id", "create_id", "create_dt", "update_id", "update_dt"]
    },
    {
        "folder": "memberScore",
        "prefix": "memberScore",
        "model": "TeamMemberScoreL",
        "pks": ["member_uid", "team_uid", "year", "score_cd"],
        "auto_pks": [],
        "cols": ["member_uid", "team_uid", "year", "score_cd", "score_val", "create_id", "create_dt", "update_id", "update_dt"]
    },
    {
        "folder": "payment",
        "prefix": "payment",
        "model": "TeamPaymentL",
        "pks": ["team_uid", "payment_cd", "team_account_seq"],
        "auto_pks": [],
        "cols": ["team_uid", "payment_cd", "team_account_seq", "amount", "create_id", "create_dt", "update_id", "update_dt"]
    },
    {
        "folder": "record",
        "prefix": "record",
        "model": "TeamRecordL",
        "pks": ["team_uid", "vote_uid", "play_date"],
        "auto_pks": [],
        "cols": ["team_uid", "vote_uid", "play_date", "member_uid", "goal_cnt", "asist_cnt", "create_id", "create_dt", "update_id", "update_dt"]
    },
    {
        "folder": "schedule",
        "prefix": "schedule",
        "model": "TeamScheduleL",
        "pks": ["vote_seq", "team_uid"],
        "auto_pks": ["vote_seq"],
        "cols": ["vote_seq", "team_uid", "play_date", "play_start_time", "play_end_time", "vote_period_from", "vote_period_to", "vote_end_yn", "create_id", "create_dt", "update_id", "update_dt"]
    },
    {
        "folder": "stardium",
        "prefix": "stardium",
        "model": "TeamStartdiumL",
        "pks": ["team_uid", "team_stardium_seq"],
        "auto_pks": ["team_stardium_seq"],
        "cols": ["team_uid", "team_stardium_seq", "location", "start_time", "end_time", "day_cd", "main_locate_yn", "create_id", "create_dt", "update_id", "update_dt"]
    },
    {
        "folder": "vote",
        "prefix": "vote",
        "model": "TeamVoteL",
        "pks": ["vote_seq", "team_uid"],
        "auto_pks": [],
        "cols": ["vote_seq", "team_uid", "play_date", "play_start_time", "play_end_time", "member_uid", "vote_cd", "create_id", "create_dt", "update_id", "update_dt"]
    }
]

def make_request(m):
    out = "from pydantic import BaseModel\nfrom typing import Optional\n\n"
    
    # Search
    out += f"class {m['prefix'].capitalize()}SearchRequest(BaseModel):\n"
    for c in m['pks']:
        out += f"    {c}: Optional[str] = None\n"
    if not m['pks']: out += "    pass\n"
    out += "\n"
    
    # Insert
    out += f"class {m['prefix'].capitalize()}InsertRequest(BaseModel):\n"
    for c in m['cols']:
        if c in ['create_id', 'create_dt', 'update_id', 'update_dt'] or c in m['auto_pks']: continue
        if c in m['pks']:
            out += f"    {c}: str\n"
        else:
            out += f"    {c}: Optional[str] = None\n"
    out += "\n"
    
    # Update
    out += f"class {m['prefix'].capitalize()}UpdateRequest(BaseModel):\n"
    for c in m['cols']:
        if c in ['create_id', 'create_dt', 'update_id', 'update_dt']: continue
        if c in m['pks']:
            if c in m['auto_pks']:
                out += f"    {c}: int\n"
            else:
                out += f"    {c}: str\n"
        else:
            out += f"    {c}: Optional[str] = None\n"
    out += "\n"
    
    # Delete
    out += f"class {m['prefix'].capitalize()}DeleteRequest(BaseModel):\n"
    for c in m['pks']:
        if c in m['auto_pks']:
            out += f"    {c}: int\n"
        else:
            out += f"    {c}: str\n"
            
    return out

def make_response(m):
    out = "from pydantic import BaseModel, ConfigDict\nfrom typing import Optional\nfrom datetime import datetime\n\n"
    out += f"class {m['prefix'].capitalize()}Response(BaseModel):\n"
    for c in m['cols']:
        out += f"    {c}: Optional[str] = None\n"
    out += "\n    model_config = ConfigDict(from_attributes=True)\n\n"
    
    out += "class MessageResponse(BaseModel):\n    message: str\n"
    return out

def make_service(m):
    out = "from sqlalchemy.ext.asyncio import AsyncSession\nfrom sqlalchemy import select, delete\nfrom datetime import datetime\n"
    out += f"from models.{m['model']} import {m['model']}\n"
    out += f"from {m['folder']} import {m['prefix']}Request\n\n"
    
    # Get
    out += f"async def get(db: AsyncSession, req: {m['prefix']}Request.{m['prefix'].capitalize()}SearchRequest):\n"
    out += f"    query = select({m['model']})\n"
    for c in m['pks']:
        out += f"    if req.{c} is not None:\n        query = query.filter({m['model']}.{c} == req.{c})\n"
    out += "    result = await db.execute(query)\n"
    out += "    return result.scalars().all()\n\n"
    
    # Insert
    out += f"async def insert(db: AsyncSession, req: {m['prefix']}Request.{m['prefix'].capitalize()}InsertRequest, session_id: str):\n"
    out += "    now = datetime.now()\n"
    out += f"    obj = {m['model']}(\n"
    for c in m['cols']:
        if c in m['auto_pks']: continue
        if c == 'create_id' or c == 'update_id':
            out += f"        {c}=session_id,\n"
        elif c == 'create_dt' or c == 'update_dt':
            out += f"        {c}=now,\n"
        else:
            out += f"        {c}=req.{c},\n"
    out += "    )\n"
    out += "    db.add(obj)\n"
    out += "    await db.commit()\n"
    out += "    return obj\n\n"
    
    # Update
    out += f"async def update(db: AsyncSession, req: {m['prefix']}Request.{m['prefix'].capitalize()}UpdateRequest, session_id: str):\n"
    out += f"    query = select({m['model']})\n"
    for c in m['pks']:
        out += f"    query = query.filter({m['model']}.{c} == req.{c})\n"
    out += "    result = await db.execute(query)\n"
    out += "    obj = result.scalars().first()\n"
    out += "    if not obj: raise ValueError('Not found')\n"
    
    for c in m['cols']:
        if c in m['pks'] or c in ['create_id', 'create_dt', 'update_id', 'update_dt']: continue
        out += f"    if req.{c} is not None: obj.{c} = req.{c}\n"
    
    out += "    if hasattr(obj, 'update_id'): obj.update_id = session_id\n"
    out += "    if hasattr(obj, 'update_dt'): obj.update_dt = datetime.now()\n"
    out += "    await db.commit()\n"
    out += "    return obj\n\n"
    
    # Delete
    out += f"async def delete_obj(db: AsyncSession, req: {m['prefix']}Request.{m['prefix'].capitalize()}DeleteRequest):\n"
    out += f"    query = delete({m['model']})\n"
    for c in m['pks']:
        out += f"    query = query.where({m['model']}.{c} == req.{c})\n"
    out += "    await db.execute(query)\n"
    out += "    await db.commit()\n"
    return out

def make_controller(m):
    out = "from fastapi import APIRouter, Depends, HTTPException, Request\nfrom sqlalchemy.ext.asyncio import AsyncSession\nfrom typing import List\n"
    out += "from database import get_db\n"
    out += f"from {m['folder']}.{m['prefix']}Request import *\n"
    out += f"from {m['folder']}.{m['prefix']}Response import *\n"
    out += f"from {m['folder']} import {m['prefix']}Service\n\n"
    
    out += f"router = APIRouter(prefix='/{m['folder']}', tags=['{m['folder'].capitalize()}'])\n\n"
    out += "def get_session_userid(request: Request) -> str:\n"
    out += "    return request.session.get('userid', 'test_user')\n\n"
    
    out += f"@router.get('/search', response_model=List[{m['prefix'].capitalize()}Response])\n"
    out += f"async def search(req: {m['prefix'].capitalize()}SearchRequest = Depends(), db: AsyncSession = Depends(get_db)):\n"
    out += f"    return await {m['prefix']}Service.get(db, req)\n\n"
    
    out += f"@router.post('/insert', response_model=MessageResponse)\n"
    out += f"async def insert(req: {m['prefix'].capitalize()}InsertRequest, request: Request, db: AsyncSession = Depends(get_db)):\n"
    out += f"    await {m['prefix']}Service.insert(db, req, get_session_userid(request))\n"
    out += f"    return MessageResponse(message='Insert Success')\n\n"
    
    out += f"@router.post('/update', response_model=MessageResponse)\n"
    out += f"async def update(req: {m['prefix'].capitalize()}UpdateRequest, request: Request, db: AsyncSession = Depends(get_db)):\n"
    out += "    try:\n"
    out += f"        await {m['prefix']}Service.update(db, req, get_session_userid(request))\n"
    out += f"        return MessageResponse(message='Update Success')\n"
    out += "    except ValueError:\n"
    out += "        raise HTTPException(404, 'Not found')\n\n"
    
    out += f"@router.post('/delete', response_model=MessageResponse)\n"
    out += f"async def delete(req: {m['prefix'].capitalize()}DeleteRequest, request: Request, db: AsyncSession = Depends(get_db)):\n"
    out += f"    await {m['prefix']}Service.delete_obj(db, req)\n"
    out += f"    return MessageResponse(message='Delete Success')\n\n"
    
    return out

for m in modules:
    os.makedirs(m['folder'], exist_ok=True)
    with open(f"{m['folder']}/{m['prefix']}Request.py", "w", encoding="utf-8") as f: f.write(make_request(m))
    with open(f"{m['folder']}/{m['prefix']}Response.py", "w", encoding="utf-8") as f: f.write(make_response(m))
    with open(f"{m['folder']}/{m['prefix']}Service.py", "w", encoding="utf-8") as f: f.write(make_service(m))
    with open(f"{m['folder']}/{m['prefix']}Controller.py", "w", encoding="utf-8") as f: f.write(make_controller(m))

print("Scaffolding complete!")

