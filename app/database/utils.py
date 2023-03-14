from ..database import models, queries 
from ..utils import schemas
from .database import Base
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext
from typing import List, Optional


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(
    password: str
    ) -> str:
    return pwd_context.hash(password)


def verify(
    plain_password: str, 
    hashed_password: str
    ) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def is_user_admin(
    db: Session, 
    current_user_id: int,
    hardcoded_user_id: int = 1, 
    hardcoded_group_id: int = 1
    ) -> bool:

    if current_user_id == hardcoded_user_id:
        return True

    users_data = db.query(models.User.id).filter(models.User.group_id==hardcoded_group_id)
    users_allowed = [id[0] for id in users_data] 
    
    if current_user_id in users_allowed:
        return True
    
    return False


def is_user_status_locked(
    db: Session, 
    current_user_id: int, 
    user_affected_id: int, 
    hardcoded_user_id: int = 1,
    hardcoded_group_id: List[int] = [1]
    ) -> bool:
    
    if user_affected_id == hardcoded_user_id:
        return True
    
    if user_affected_id == current_user_id:
        return True

    users_data = db.query(models.User.id).filter(models.User.group_id.in_(hardcoded_group_id)).all()
    users_id_in_locked_groups: List[int] = [id[0] for id in users_data]

    if user_affected_id in users_id_in_locked_groups:
        return True

    return False


def is_user_available(db: Session, new_user: schemas.UserCreate)->bool:
    if db.query(models.User).filter(models.User.email==new_user.email).first():
        return False
    return True


def is_user_allowed_to_change_password(db: Session, affected_user_id: int, current_user_id: int) -> bool:
    if is_user_admin(db,current_user_id) or current_user_id==affected_user_id:
        return True
    return False


def raise_404_if_register_not_exist(
    register: Base,
    id: int,
    name_String: str
    ) -> None:
    if not register:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  detail=f"{name_String.upper()} with ID: {id} does not exist")
    return None


def raise_403_if_user_not_authorized(
    register: Base, 
    current_user_id: int
    ) -> None:
    if register.created_by_user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,  detail="Not Authorized to perform requested action")
    return None


def raise_403_if_user_is_not_admin(
    db: Session, 
    current_user: models.User, 
    action_string: Optional[str] = None
    ) -> None:

    if action_string is not None:
        action_string = " - " + action_string

    if not is_user_admin(db,current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action{action_string}"
        )

    return None


def raise_403_if_user_must_stay_Active(
    db: Session, 
    current_user: models.User, 
    user_affected: models.User
    ) -> None:

    if is_user_status_locked(db,current_user.id,user_affected.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unable to perform requested action - User must remain active"
        )
    
    return None


def raise_403_if_user_exists(db: Session, new_user: schemas.UserCreate)->None:
    
    if not is_user_available(db,new_user):
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Unable to perform requested action - Create User - User already exists"
        )

    return None


def raise_403_if_user_not_allowed_to_change_password(db: Session, user: models.User, current_user_id) -> None:
    if not is_user_allowed_to_change_password(db, user.id, current_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action - Change User Password"
        )
    return None
    

def raise_400_if_user_not_active(db: Session, user: models.User) -> None:    
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to perform requested action - User is Inactive"
        )     
    return None
    

def raise_404_if_group_id_invalid(db: Session, group_id: int) -> None: 
    group_id_exists = db.query(models.UserGroup).filter(models.UserGroup.id==group_id).first()    
    if not group_id_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unable to perform requested action - User Group ID: {group_id} does not exist"
        )     
    return None



def _change_user_state(db: Session, updated_user_fields: schemas.UserChangeState, affected_user: models.User):
    if updated_user_fields.active == affected_user.active:
        return affected_user
    if updated_user_fields.active is None:
        updated_user_fields.active = not affected_user.active

    user_register = db.query(models.User).filter(models.User.id == affected_user.id).first()
    user_register.active = updated_user_fields.active
    db.commit()
    
    return user_register


def _change_user_password(db: Session, id: int, updated_user_fields: schemas.UserChangePassword):
    affected_user_register = db.query(models.User).filter(models.User.id==id).first()
    affected_user_register.password = hash(updated_user_fields.password)
    db.commit()
    db.refresh(affected_user_register)
    return affected_user_register


def _change_user_group(db: Session, id: int, updated_user_fields: schemas.UserChangeGroup):
    affected_user_register = db.query(models.User).filter(models.User.id==id).first()
    affected_user_register.group_id= updated_user_fields.group_id
    db.commit()
    db.refresh(affected_user_register)
    return affected_user_register


def _create_user(db: Session, new_user:schemas.UserCreate):

    new_user_register = models.User(**new_user.dict())
    new_user_register.password = hash(new_user.password)
    new_user_register.group_id = 2
    db.add(new_user_register)
    db.commit()
    db.refresh(new_user_register)
    return new_user_register


def projectHastTask(db: Session, project_id: int):
    q = db.query(models.Task).filter(models.Task.project_id==project_id).first()
    return True if q is not None else False
