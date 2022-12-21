from fastapi import status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import models, queries, utils, oauth2
from ..database.database import get_db
from ..utils import schemas

router = APIRouter(
    prefix="/tasks",
    tags=['Tasks']
    )

@router.get("/project/{id}", response_model=List[schemas.TaskResponse])
async def get_tasks_by_project(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    
    project = db.query(models.Project).filter(models.Project.id == id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Project found with ID: {id}")
    if current_user.id != 1 and current_user.id != project.created_by_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,  detail="Not Authorized to perform requested action - Retrieve Tasks by Project id - Project created by another User")

    
    tasks_query = db.query(models.Task).filter(models.Task.project_id == id).order_by(models.Task.created_at)
    tasks = tasks_query.all()
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Tasks found for Project with ID: {id}")

    return tasks

@router.post("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.TaskResponse)
async def create_task(id: int, task: schemas.TaskCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Project found with ID: {id}")
    active = False
    if project.active == 'true':
        active=True

    if not active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,  detail="Not Authorized to perform requested action - Create Task - Linked Project Inactive")
    if current_user.id != 1 and current_user.id != project.created_by_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,  detail="Not Authorized to perform requested action - Create Task - Linked Project created by another User")

    task.created_by_user_id = current_user.id
    task.active=1
    task.state_id=1
    task.project_id=id

    #new_task = queries.insert_register(models.Task, db, task)

    new_register = models.Task(**task.dict())
    db.add(new_register)
    db.commit()
    db.refresh(new_register)

    return new_register

@router.get("/{id}", response_model=schemas.TaskResponse)
async def get_task(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    task = queries.get_register_by_id(models.Task, db, id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Task found with ID: {id}")
    project = db.query(models.Project).filter(models.Project.id == task.project_id).first()

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task is not linked to project")
    if not project.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,  detail="Not Authorized to perform requested action - Retrieve Task - Linked Project Inactive")
       
    if current_user.id != 1 and current_user.id != project.created_by_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,  detail="Not Authorized to perform requested action - Retrieve Task - Linked Project created by another User")

    return task


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: int,  db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    task_query = queries.__get_register_by_id(models.Task, db, id)

    task = task_query.first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Task found with ID: {id}")
    project = db.query(models.Project).filter(models.Project.id == task.project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task is not linked to project")
    active = False
    if project.active == 'true':
        active = True
    
    if not active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,  detail="Not Authorized to perform requested action - Delete Task - Linked Project Inactive")
    if current_user.id != 1 and current_user.id != project.created_by_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,  detail="Not Authorized to perform requested action - Delete Task - Linked Project created by another User")
    return queries.delete_register(task_query, db)


@router.put("/{id}", response_model=schemas.TaskResponse)
async def update_task(id: int, updated_task_fields: schemas.TaskUpdate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)) :
    task_query = queries.__get_register_by_id(models.Task, db, id)
    task = task_query.first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Task found with ID: {id}")
    project = db.query(models.Project).filter(models.Project.id == task.project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task is not linked to project")
    if not project.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,  detail="Not Authorized to perform requested action - Update Task - Linked Project Inactive")
    if current_user.id != 1 and current_user.id != project.created_by_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,  detail="Not Authorized to perform requested action - Update Task - Linked Project created by another User")

   
    return queries.update_register(task_query, db, updated_task_fields)


