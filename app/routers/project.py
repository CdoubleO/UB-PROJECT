from fastapi import status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import models, queries, utils, oauth2
from ..database.database import get_db
from ..utils import schemas

router = APIRouter(
    prefix="/projects",
    tags=['Projects']
    )

@router.get("/", response_model=List[schemas.ProjectResponse])
async def get_projects(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    if current_user.id == 1 or current_user.group_id == 1:
        projects = db.query(models.Project).order_by(models.Project.id).all()
    else:
        projects = db.query(models.Project).filter(models.Project.created_by_user_id == current_user.id).order_by(models.Project.id).all()
    
    if not projects:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  detail="No Projects Found")

    return projects

@router.post("/title", response_model=List[schemas.ProjectResponse])
async def get_projects(project_filter: schemas.ProjectSearchByTitle, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    if current_user.id == 1 or current_user.group_id == 1:
        projects = db.query(models.Project).filter(models.Project.title.ilike(f'%{project_filter.title}%')).order_by(models.Project.id).all()
    else:
        projects = db.query(models.Project).filter(models.Project.created_by_user_id == current_user.id, models.Project.title.ilike(f'%{project_filter.title}%')).order_by(models.Project.id).all()
    
    if not projects:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  detail="No Projects Found")

    return projects

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ProjectResponse)
async def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    
    project.created_by_user_id = current_user.id
    project.state_id = 1
    #new_project = queries.insert_register(models.Project, db, project)
    new_register = models.Project(**project.dict())
    db.add(new_register)
    db.commit()
    db.refresh(new_register)

    return new_register

@router.get("/{id}", response_model=schemas.ProjectResponse)
async def get_project(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    project = queries.get_register_by_id(models.Project, db, id)

    utils.raise_404_if_register_not_exist(project, id, 'Project')

    return project


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(id: int,  db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    project_query = queries.__get_register_by_id(models.Project, db, id)

    project = project_query.first()

    if current_user.id != 1 and current_user.id != project.created_by_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,  detail="Not Authorized to perform requested action - Project created by another User")

    utils.raise_404_if_register_not_exist(project, id, 'Project')

    utils.raise_403_if_user_not_authorized(project, current_user.id)

    active = False
    if str(project.active) == 'true':
        active = True
    
    if not active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action - Project Inactive")
    
    
    return queries.delete_register(project_query, db)


@router.put("/{id}", response_model=schemas.ProjectResponse)
async def update_project(id: int, updated_project_fields: schemas.ProjectCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)) :
    project = queries.__get_register_by_id(models.Project, db, id)
    project_data = project.first()

    utils.raise_404_if_register_not_exist(project_data, id, 'Project')

    if current_user.id != 1 and current_user.id != project_data.created_by_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,  detail="Not Authorized to perform requested action - Project created by another User")
    
    active = False
    if str(project_data.active) == 'true':
        active = True
    
    if updated_project_fields.active is True:
        active = True 
    
    if not active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action - Project Inactive")
    
    updated_project_fields.state_id = project_data.state_id
    # updated_project_fields.active = bool(project_data.active)
    updated_project_fields.created_by_user_id = project_data.created_by_user_id


    return queries.update_register(project, db, updated_project_fields)


@router.put("/state/{id}", response_model=schemas.ProjectResponse)
async def change_project_state(id: int, updated_project_fields: schemas.ProjectChangeState, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)) :
    project = queries.__get_register_by_id(models.Project, db, id)
    project_data = project.first()

    utils.raise_404_if_register_not_exist(project_data, id, 'Project')
    

    if current_user.id != project_data.id:
        utils.raise_403_if_user_is_not_admin(db, current_user)
    active = False
    if str(project_data.active) == 'true':
        active = True
    
    if not active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action - Project Inactive")
    
    project_data.state_id = updated_project_fields.state_id
    db.commit()

    return project_data
