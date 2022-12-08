from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ProjectBase(BaseModel):
    title: str
    description: str 
    active: bool = True
    state_id: int = 1
    #created_by_user_id: int


class ProjectCreate(ProjectBase):
    created_by_user_id: int


class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    title: str
    description: str 
    active: bool = True
    project_id: int
    state_id: int = 1
    #created_by_user_id: int


class TaskCreate(TaskBase):
    created_by_user_id: int

class TaskUpdate(BaseModel):
    title: str
    description: str 


class TaskResponse(TaskBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    active: bool = True


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserChangeState(BaseModel):
    active: Optional[bool] = None


class UserChangePassword(UserCreate):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None