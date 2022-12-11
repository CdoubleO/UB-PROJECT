from fastapi import FastAPI, Request, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from .database import models
from .database.database import engine, get_db
from .routers import user, project, auth, task
from .config import settings
from sqlalchemy.orm import Session
from .templates.forms import LoginForm
from .database import utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
# models.Base.metadata.create_all(bind=engine)

origins = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


templates = Jinja2Templates(directory="app/templates/")

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(project.router)
app.include_router(task.router)

@app.get("/dashboard", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard/login", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/dashboard/login", response_class=HTMLResponse)
async def login(response: Response, request: Request, db: Session = Depends(get_db), user_credentials: OAuth2PasswordRequestForm = Depends(),):
 
    form = LoginForm(request)
    await form.load_data()

    if await form.is_valid():
        try:
            user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

            if not user or not utils.verify(user_credentials.password, user.password) or not user.active:
                return templates.TemplateResponse("login.html", {"request":request, "errors":"invaid credential"})
            
            access_token = oauth2.create_access_token(data = {"user_id": user.id})
            response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
            print(access_token)
            print(response)
            return templates.TemplateResponse("login.html", {"request":request, "msg":"Login Succesful"})
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("login.html", form.__dict__)
    
        
    return templates.TemplateResponse("login.html", form.__dict__)
