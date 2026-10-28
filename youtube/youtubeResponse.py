from pydantic import BaseModel

class YoutubeVideoResponse(BaseModel):
    video_id: str
    title: str
    link: str
    thumbnail: str
    published: str
