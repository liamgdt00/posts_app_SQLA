from fastapi import FastAPI

from . import  schemas
from .database import engine
from .routers import posts_router, users_router, auth

# App instance
app = FastAPI()
app.include_router(posts_router.router)
app.include_router(users_router.router)
app.include_router(auth.router)

# From the corresponding mapped classes, creates the tables in DB
schemas.Base.metadata.create_all(bind = engine)

@app.get('/')
def root():
    return {'Message' : 'Hello World'}