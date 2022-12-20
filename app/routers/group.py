from fastapi import status, Depends, APIRouter, HTTPException
from sqlalchemy import and_, or_, not_
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import models, queries, utils, oauth2
from ..database.database import get_db
from ..utils import schemas



router = APIRouter(
    prefix="/userGroup",
    tags=['UserGroups']
    )


@router.get("/", response_model=List[schemas.UserGroupResponse])
async def get_groups(filter_by_status: Optional[bool] = None, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    utils.raise_403_if_user_is_not_admin(db, current_user, action_string="Retrieve User Groups")

    groups = db.query(models.UserGroup)

    if filter_by_status is False:
        return groups.filter(models.UserGroup.active == False).order_by(models.UserGroup.id).all()

    if filter_by_status is True:
        return groups.filter(models.UserGroup.active == True).order_by(models.UserGroup.id).all()

    return groups.order_by(models.UserGroup.id).all()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserGroupResponse)
async def create_group(new_group: schemas.UserGroupCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    utils.raise_403_if_user_is_not_admin(db,current_user,action_string='Create UserGroup')
    

    new_group_register = models.UserGroup(**new_group.dict())
    new_group_register.active = 1
    db.add(new_group_register)
    db.commit()
    db.refresh(new_group_register)
    return new_group_register


@router.put("/state/{id}", response_model=schemas.UserGroupResponse)
async def change_user_group_state(id: int, updated_group_fields: schemas.UserGroupChangeState, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    utils.raise_403_if_user_is_not_admin(db,current_user,action_string='Change User State')

    group = queries.get_register_by_id(models.UserGroup, db, id)
    utils.raise_404_if_register_not_exist(group, id, 'UserGroup')

    if id == 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unable to perform requested action - UserGroup must remain active"
        )
    

    if updated_group_fields.active is None:
        updated_group_fields.active = not group.active
    if updated_group_fields.active == group.active:
        return group

    group_register = db.query(models.UserGroup).filter(models.UserGroup.id == id).first()
    group_register.active = updated_group_fields.active
    db.commit()
    
    return group_register
