from fastapi import status, Depends, APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..database import models, utils, oauth2
from ..utils import schemas

router = APIRouter(
    prefix="/login",
    tags=['Authentication']
    )


@router.post('/', status_code=status.HTTP_200_OK ,response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user or not utils.verify(user_credentials.password, user.password) or not user.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/cookie', status_code=status.HTTP_200_OK ,response_model=schemas.Token)
async def create_cookie(req: Request,db: Session = Depends(get_db)):
    if req.headers['Content-Type'] == 'application/json':
        user_credentials = OAuth2PasswordRequestForm(** await req.json())
    elif req.headers['Content-Type'] == 'multipart/form-data':
        user_credentials = OAuth2PasswordRequestForm(** await req.form())
    elif req.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        user_credentials = OAuth2PasswordRequestForm(** await req.form())

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user or not utils.verify(user_credentials.password, user.password) or not user.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    response = JSONResponse(content={"message":"test"})
    response.set_cookie(key="access_token", value=access_token)
    return response


@router.get('/', status_code=status.HTTP_200_OK , response_model=schemas.UserResponse)
async def isLogged(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()

    if not user or not user.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    return user


    