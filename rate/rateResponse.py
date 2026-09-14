from pydantic import BaseModel

class RateResponse(BaseModel):
    team_uid: str
    member_uid: str
    member_name: str
    user_id: str | None = None
    total_matches: int
    attend_count: int
    absent_count: int
    no_vote_count: int
    attend_rate: float
    total_score: int
    rank_num: int
    status_cd: str | None = None
    code_name: str | None = None

