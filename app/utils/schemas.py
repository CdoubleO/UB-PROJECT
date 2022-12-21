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


class ProjectChangeState(BaseModel):
    state_id: int

class ProjectSearchByTitle(BaseModel):
    title: str

class ProjectStateResponse(BaseModel):
    id: int
    description: str
    active: bool

    class Config:
        orm_mode = True


class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    created_by_user_id: int
    state: ProjectStateResponse

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

class UserBase(BaseModel):
    email: EmailStr
    #active: bool = True


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    group_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    owner: UserResponse
    state: ProjectStateResponse

    class Config:
        orm_mode = True








class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserChangeState(BaseModel):
    active: Optional[bool] = None


class UserChangePassword(BaseModel):
    pass


class UserChangePassword(BaseModel):
    password: str


class UserChangeGroup(BaseModel):
    group_id: int


class UserGroupBase(BaseModel):
    title: str
    description: str 
    

class UserGroupCreate(UserGroupBase):
    pass


class UserGroupResponse(UserGroupBase):
    id: int
    active: bool = True
    
    class Config:
        orm_mode = True


class UserGroupChangeState(BaseModel):
    active: Optional[bool] = None

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None