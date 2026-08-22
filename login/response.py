from pydantic import BaseModel

class UserResponse(BaseModel):
    userid: str
    username: str

class MessageResponse(BaseModel):
    message: str
    userid: str | None = None
    username: str | None = None

