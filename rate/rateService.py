from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, bindparam
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from zoneinfo import ZoneInfo
from rate.rateRequest import RateSearchRequest
from rate.rateResponse import RateResponse

async def get_streaks(db: AsyncSession, member_uids: set, team_uid: Optional[str], today: Optional[str]) -> Dict[str, Tuple[int, int]]:
    """멤버별 (연속 참석 수, 연속 불참·미투표 수). 오늘 이전 경기를 최근부터 세고 미진행(04)은 건너뜀 (연도 구분 없음)"""
    if not member_uids:
        return {}
    today = today or datetime.now(ZoneInfo('Asia/Seoul')).strftime('%Y%m%d')
    sql = """
        SELECT v.member_uid, v.vote_cd
        FROM team_vote_l v
        JOIN team_schedule_l s ON s.team_uid = v.team_uid AND s.vote_seq = v.vote_seq
        WHERE s.play_date < :today
          AND v.vote_cd IN ('01', '02', '03')
          AND v.member_uid IN :member_uids
    """
    params = {"today": today, "member_uids": list(member_uids)}
    if team_uid:
        sql += " AND v.team_uid = :team_uid"
        params["team_uid"] = team_uid
    sql += " ORDER BY v.member_uid, s.play_date DESC, s.vote_seq DESC"

    query = text(sql).bindparams(bindparam("member_uids", expanding=True))
    return count_streaks((await db.execute(query, params)).fetchall())

def count_streaks(rows) -> Dict[str, Tuple[int, int]]:
    """(member_uid, vote_cd) 를 멤버별 최근 경기 순으로 받아 연속 참석 / 연속 불참·미투표 수를 셈"""
    streaks: Dict[str, Tuple[int, int]] = {}
    done = set()  # 연속이 끊긴 멤버
    for member_uid, vote_cd in rows:
        if member_uid in done:
            continue
        attend, miss = streaks.get(member_uid, (0, 0))
        if vote_cd == '02' and miss == 0:
            streaks[member_uid] = (attend + 1, 0)
        elif vote_cd in ('01', '03') and attend == 0:
            streaks[member_uid] = (0, miss + 1)
        else:
            done.add(member_uid)
    return streaks

async def get_rates(db: AsyncSession, req: RateSearchRequest) -> List[RateResponse]:
    # Construct base query
    base_sql = """
        WITH team_stats AS (
            SELECT 
                m.team_uid,
                m.member_uid,
                m.member_name,
                m.user_id,
                m.status_cd,
                (SELECT code_name FROM common_cd_b WHERE code = m.status_cd AND group_cd = 'status_cd' LIMIT 1) AS code_name,
                COUNT(v.vote_seq) AS total_matches,
                COALESCE(SUM(CASE WHEN v.vote_cd = '02' THEN 1 ELSE 0 END), 0) AS attend_count,
                COALESCE(SUM(CASE WHEN v.vote_cd = '03' THEN 1 ELSE 0 END), 0) AS absent_count,
                COALESCE(SUM(CASE WHEN v.vote_cd = '01' THEN 1 ELSE 0 END), 0) AS no_vote_count
            FROM team_member_l m
            JOIN team_info_b t ON m.team_uid = t.team_uid
            LEFT JOIN team_schedule_l s ON s.team_uid = m.team_uid AND substring(s.play_date from 1 for 4) = :year
            LEFT JOIN team_vote_l v ON v.vote_seq = s.vote_seq AND v.team_uid = m.team_uid AND v.member_uid = m.member_uid
                AND v.vote_cd IN ('01', '02', '03')
            WHERE m.terminate_dt IS NULL
    """
    
    params = {"year": req.year}
    
    if req.team_uid:
        base_sql += " AND t.team_uid = :team_uid"
        params["team_uid"] = req.team_uid
    if req.teamname:
        base_sql += " AND t.team_name = :teamname"
        params["teamname"] = req.teamname
        
    base_sql += """
            GROUP BY m.team_uid, m.member_uid, m.member_name, m.user_id, m.status_cd
        ),
        ranked_stats AS (
            SELECT 
                ts.*,
                CASE WHEN ts.total_matches > 0 THEN 
                     ROUND(ts.attend_count * 100.0 / ts.total_matches, 2)
                ELSE 0 END AS attend_rate,
                (ts.attend_count * 3) + (ts.absent_count * 1) + (ts.no_vote_count * -2) AS total_score,
                RANK() OVER(
                    PARTITION BY ts.team_uid 
                    ORDER BY 
                        ((ts.attend_count * 3) + (ts.absent_count * 1) + (ts.no_vote_count * -2)) DESC,
                        CASE WHEN ts.total_matches > 0 THEN (ts.attend_count * 100.0 / ts.total_matches) ELSE 0 END DESC, 
                        ts.attend_count DESC,
                        ts.total_matches DESC
                ) AS rank_num
            FROM team_stats ts
            WHERE ts.total_matches > 0
        )
        SELECT * FROM ranked_stats
        WHERE 1=1
    """
    
    if req.member_uid:
        base_sql += " AND member_uid = :member_uid"
        params["member_uid"] = req.member_uid
    if req.member_name:
        base_sql += " AND member_name = :member_name"
        params["member_name"] = req.member_name
        
    base_sql += " ORDER BY rank_num;"
    
    result = await db.execute(text(base_sql), params)
    rows = result.fetchall()
    streaks = await get_streaks(db, {row.member_uid for row in rows}, req.team_uid, req.today)

    return [
        RateResponse(
            team_uid=row.team_uid,
            member_uid=row.member_uid,
            member_name=row.member_name,
            user_id=row.user_id,
            total_matches=row.total_matches or 0,
            attend_count=row.attend_count or 0,
            absent_count=row.absent_count or 0,
            no_vote_count=row.no_vote_count or 0,
            attend_rate=float(row.attend_rate) if row.attend_rate else 0.0,
            total_score=row.total_score or 0,
            rank_num=row.rank_num or 0,
            status_cd=row.status_cd,
            code_name=row.code_name or (
                '활동' if row.status_cd == '01' else 
                '부상' if row.status_cd == '02' else 
                '휴식' if row.status_cd == '03' else ''
            ),
            attend_streak=streaks.get(row.member_uid, (0, 0))[0],
            miss_streak=streaks.get(row.member_uid, (0, 0))[1],
        ) for row in rows
    ]

