from fastapi import FastAPI, Depends, status, HTTPException, Response, Request
from . import models, schemas
from .database import engine,  get_db
from sqlalchemy.orm import Session
from sqlalchemy import inspect, Inspector
from typing import Optional, Annotated
import sqlite3
from sqlalchemy.exc import IntegrityError, DBAPIError
from .utils import get_column_query_constraint_failure
# App instance
app = FastAPI()

inspector = inspect(engine)
constraints = inspector.get_unique_constraints('users')
print('before constraints')
print(f'constraints = {constraints}')
# From the corresponding mapped classes, creates the tables in DB 
schemas.Base.metadata.create_all(bind = engine)





# GET request to return all records in the Posts table
@app.get('/posts', response_model=list[models.ShowPost])
def get_posts(db : Session = Depends(get_db)):
    posts = db.query(schemas.Posts).all()
    return posts

# Get request to return a specfic record based on id
@app.get('/posts/{post_id}', response_model=models.ShowPost)
def get_post(post_id: int, db : Session = Depends(get_db)):
    post = db.query(schemas.Posts).filter(schemas.Posts.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id : {post_id} not found')
    return post

# POST request to create a new record of post in the Posts table
# uses PostCreate as request body structure, Depends returns a pydantic object
@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model= models.ShowPost)
def create_post(request : models.PostCreate, db :Session = Depends(get_db)):
    new_post = schemas.Posts(title = request.title, content = request.content, published = request.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@app.delete('/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id : int , db : Session = Depends(get_db)):
    post_query = db.query(schemas.Posts).filter(schemas.Posts.id == post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id : {post_id} not found')
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.put('/posts/{post_id}', status_code=status.HTTP_202_ACCEPTED, response_model=models.ShowPost)
def update_post(post_id : int, request : models.PostCreate, db : Session = Depends(get_db)):
    # updated_post = schemas.Posts(request.model_dump(exclude_unset=True))
    post_query = db.query(schemas.Posts).filter(schemas.Posts.id == post_id)
    print(post_query)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id : {post_id} not found')
    num_rows = post_query.update(request.model_dump(exclude_unset=True))
    print(f'Deleted {num_rows} rows')
    post = post_query.first()
    db.commit()
    # refreshes the in-memory state of object to match database
    db.refresh(post)
    return post


@app.post('/users', status_code=status.HTTP_201_CREATED)
def create_user(request : models.UserCreate, db : Session = Depends(get_db)):
    new_user = schemas.Users(**request.model_dump())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError as e:
        error_column = get_column_query_constraint_failure(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f'This {error_column} already exists, please select a new {error_column} ')

    return new_user


@app.get('/users/{user_id}')
def get_user(user_id : int , db : Session = Depends(get_db)):
    user = db.query(schemas.Users).filter(schemas.Users.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'User with user_id : {user_id} not found')
    return user

@app.get('/users')
def get_users(db : Session = Depends(get_db)):
    users = db.query(schemas.Users).all()
    return users

@app.delete('/users/{id}')
def delete_user(id : int, db : Session = Depends(get_db)):
    user_query = db.query(schemas.Users).filter(schemas.Users.user_id == id)
    print(user_query)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'User with user_id : {id} not found')
    
    num_rows = user_query.delete(synchronize_session=False)
    print(f'Deleted {num_rows} rows')
    db.commit()