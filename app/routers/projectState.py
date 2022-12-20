from fastapi import status, Depends, APIRouter, HTTPException
from sqlalchemy import and_, or_, not_
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import models, queries, utils, oauth2
from ..database.database import get_db
from ..utils import schemas



router = APIRouter(
    prefix="/projectState",
    tags=['ProjectStates']
    )



@router.get("/", response_model=List[schemas.ProjectStateResponse])
async def get_project_states(filter_by_status: Optional[bool] = None, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    states = db.query(models.ProjectState)

    if filter_by_status is None:
        return states.order_by(models.ProjectState.id).all()
    
    return states.filter(models.ProjectState.active == filter_by_status).order_by(models.ProjectState.id).all()

    