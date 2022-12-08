from fastapi import status, Depends, APIRouter, HTTPException
from sqlalchemy import and_, or_, not_
from sqlalchemy.orm import Session
from typing import List
from ..database import models, queries, utils, oauth2
from ..database.database import get_db
from ..utils import schemas



router = APIRouter(
    prefix="/users",
    tags=['Users']
    )

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    if current_user.id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to perform requested action - Create User"
        )
    
    user.password = utils.hash(user.password)

    new_user = queries.insert_register(models.User, db, user)

    return new_user

@router.get("/", response_model=List[schemas.UserResponse])
async def get_users(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    if current_user.id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to perform requested action - Retrieve Users"
        )

    users = db.query(models.User).filter(models.User.active == True).order_by(models.User.id).all()

    return users

@router.get("/{id}", response_model=schemas.UserResponse)
async def get_user(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    user = queries.get_register_by_id(models.User, db, id)

    if current_user.id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to perform requested action - Retrieve User"
        )

    utils.raise_404_if_register_not_exist(user, id, 'User')

    return user


@router.put("/state/{id}", response_model=schemas.UserResponse)
async def change_user_state(id: int, updated_user_fields: schemas.UserChangeState, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    utils.raise_403_if_user_is_not_admin(db,current_user,action_string='Change User State')

    user = queries.get_register_by_id(models.User, db, id)
    utils.raise_404_if_register_not_exist(user, id, 'User')

    utils.raise_403_if_user_must_stay_Active(db,current_user,user)

    # if updated_user_fields.active == user.active:
    #     return user
    # if updated_user_fields.active is None:
    #     updated_user_fields.active = not user.active

    # user_register = queries.__get_register_by_id(models.User, db, id)
    # return queries.update_register(user_register, db, updated_user_fields)

    return utils._change_user_state(db,updated_user_fields,user)


@router.put("/{id}", response_model=schemas.UserResponse)
async def change_user_password(id: int, updated_user_fields: schemas.UserChangePassword, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    user = queries.get_register_by_id(models.User, db, id)
    utils.raise_404_if_register_not_exist(user, id, 'User')

    if current_user.id != 1 or current_user.id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to perform requested action - Update User Password"
        )


    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unable to perform requested action - Update User Password - Inactive User"
        )
        
    user_register = queries.__get_register_by_id(models.User, db, id)
    updated_user_fields.password = utils.hash(user.password)

    return queries.update_register(user_register, db, updated_user_fields)
