from .database import Base
from fastapi import HTTPException, status
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def raise_404_if_register_not_exist(register: Base, id: int, name_String: str):
    if not register:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  detail=f"{name_String.upper()} with ID: {id} does not exist")
    return


def raise_403_if_user_not_authorized(register, current_user_id):
    if register.created_by_user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,  detail="Not Authorized to perform requested action")
    return


def hash(password: str) -> str:
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

