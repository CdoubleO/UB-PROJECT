from fastapi import status, Depends, APIRouter, HTTPException
from sqlalchemy import and_, or_, not_
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import models, queries, utils, oauth2
from ..database.database import get_db
from ..utils import schemas



router = APIRouter(
    prefix="/users",
    tags=['Users']
    )

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(new_user: schemas.UserCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    utils.raise_403_if_user_is_not_admin(db,current_user,action_string='Create User')
    utils.raise_403_if_user_exists(db,new_user) # if user already exist raise 403

    return utils._create_user(db, new_user)


@router.get("/", response_model=List[schemas.UserResponse])
async def get_users(filter_by_status: Optional[bool] = None, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    utils.raise_403_if_user_is_not_admin(db, current_user, action_string="Retrieve Users")

    users = db.query(models.User)
    if filter_by_status is None:
        return users.order_by(models.User.id).all()
    if filter_by_status is True:
        return users.filter(models.User.active == True).order_by(models.User.id).all()

    return users.filter(models.User.active == False).order_by(models.User.id).all()


@router.get("/{id}", response_model=schemas.UserResponse)
async def get_user(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    utils.raise_403_if_user_is_not_admin(db, current_user, action_string="Retrieve User")
    
    user = queries.get_register_by_id(models.User, db, id)
    utils.raise_404_if_register_not_exist(user, id, 'User')

    return user


@router.get("/group/{id}", response_model=List[schemas.UserResponse])
async def get_user(group_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    utils.raise_403_if_user_is_not_admin(db, current_user, action_string="Retrieve User")
    utils.raise_404_if_group_id_invalid(db,group_id)    

    users = db.query(models.User).filter(models.User.group_id==group_id).all()
    if not users:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail=f"No Users Found with Group id: {group_id}"
        )

    return users


@router.put("/state/{id}", response_model=schemas.UserResponse)
async def change_user_state(id: int, updated_user_fields: schemas.UserChangeState, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    utils.raise_403_if_user_is_not_admin(db,current_user,action_string='Change User State')

    user = queries.get_register_by_id(models.User, db, id)
    utils.raise_404_if_register_not_exist(user, id, 'User')

    utils.raise_403_if_user_must_stay_Active(db,current_user,user)

    return utils._change_user_state(db,updated_user_fields,user)


@router.put("/password/{id}", response_model=schemas.UserResponse)
async def change_user_password(id: int, updated_user_fields: schemas.UserChangePassword, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    user = queries.get_register_by_id(models.User, db, id)
    utils.raise_404_if_register_not_exist(user, id, 'User')

    utils.raise_403_if_user_not_allowed_to_change_password(db, user, current_user.id)
    utils.raise_400_if_user_not_active(db, user)

    return utils._change_user_password(db,id,updated_user_fields)


@router.put("/password/", response_model=schemas.UserResponse)
async def change_current_user_password(updated_user_fields: schemas.UserChangePassword, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    user = queries.get_register_by_id(models.User, db, current_user.id)
    utils.raise_404_if_register_not_exist(user, current_user.id, 'User')

    utils.raise_403_if_user_not_allowed_to_change_password(db, user, current_user.id)
    utils.raise_400_if_user_not_active(db, user)

    return utils._change_user_password(db,current_user.id,updated_user_fields)

@router.put("/group/{id}", response_model=schemas.UserResponse)
async def change_user_group(id: int, updated_user_fields: schemas.UserChangeGroup, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    user = queries.get_register_by_id(models.User, db, id)
    utils.raise_404_if_register_not_exist(user, id, 'User')

    utils.raise_404_if_group_id_invalid(db,updated_user_fields.group_id)

    utils.raise_403_if_user_is_not_admin(db, current_user, action_string="Retrieve User")
    utils.raise_400_if_user_not_active(db, user)

    return utils._change_user_group(db,id,updated_user_fields)