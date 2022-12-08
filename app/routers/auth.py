from fastapi import status, Depends, APIRouter, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..database import models, utils, oauth2
from ..utils import schemas

router = APIRouter(
    prefix="/login",
    tags=['Authentication']
    )


@router.post('/', response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user or not utils.verify(user_credentials.password, user.password) or not user.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}