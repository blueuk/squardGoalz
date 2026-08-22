from pydantic import BaseModel

class RegisterRequest(BaseModel):
    userid: str
    username: str
    nickname: str
    phone: str

