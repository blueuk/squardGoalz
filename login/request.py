from pydantic import BaseModel, ConfigDict, Field

class UserCreate(BaseModel):
    userid: str = Field(min_length=4, max_length=15)
    password: str = Field(min_length=8, max_length=100)
    username: str = Field(min_length=2, max_length=10)
    model_config = ConfigDict(json_schema_extra={"example": {"userid": "Woogi", "password": "my_secret_password_123!", "username": "우기"}})

class UserLogin(BaseModel):
    userid: str
    password: str
    model_config = ConfigDict(json_schema_extra={"example": {"userid": "Woogi", "password": "my_secret_password_123!"}})

