from fastapi import APIRouter, HTTPException
from typing import List

from youtube.youtubeResponse import YoutubeVideoResponse
from youtube import youtubeService

router = APIRouter(prefix="/youtube", tags=["Youtube"])

@router.get("/latest", response_model=List[YoutubeVideoResponse])
async def get_latest_videos():
    """팀 유튜브 채널의 최신 영상 목록(최대 15개)을 반환합니다."""
    try:
        return await youtubeService.get_latest_videos()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"유튜브 영상을 불러오지 못했습니다: {e}")
