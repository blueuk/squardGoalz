from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import List
from rate.rateRequest import RateSearchRequest
from rate.rateResponse import RateResponse

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
                (SELECT code_name FROM common_cd_b WHERE code = m.status_cd AND group_cd = 'MEMBER_STATUS' LIMIT 1) AS code_name,
                COUNT(v.vote_seq) AS total_matches,
                COALESCE(SUM(CASE WHEN v.vote_cd = '02' THEN 1 ELSE 0 END), 0) AS attend_count,
                COALESCE(SUM(CASE WHEN v.vote_cd = '03' THEN 1 ELSE 0 END), 0) AS absent_count,
                COALESCE(SUM(CASE WHEN v.vote_cd = '01' THEN 1 ELSE 0 END), 0) AS no_vote_count
            FROM team_member_l m
            JOIN team_info_b t ON m.team_uid = t.team_uid
            LEFT JOIN team_schedule_l s ON s.team_uid = m.team_uid AND substring(s.play_date from 1 for 4) = :year
            LEFT JOIN team_vote_l v ON v.vote_seq = s.vote_seq AND v.team_uid = m.team_uid AND v.member_uid = m.member_uid
                AND v.vote_cd IN ('01', '02', '03')
            WHERE 1=1
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
            )
        ) for row in rows
    ]

