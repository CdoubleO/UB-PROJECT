from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import models
from .database.database import engine, get_db
from .routers import user, project, auth, task
from .config import settings

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

@app.get("/")
async def root():
    return {"message": 'Hello world!'}


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(project.router)
app.include_router(task.router)
