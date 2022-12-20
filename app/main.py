from fastapi import FastAPI, Request, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from .database import models
from .database.database import engine, get_db
from .routers import user, project, auth, task, group, projectState
from .config import settings
from sqlalchemy.orm import Session
from .templates.forms import LoginForm, CreateProjectForm
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
app.include_router(group.router)
app.include_router(projectState.router)



@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


    
    