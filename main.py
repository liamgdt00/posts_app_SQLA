from fastapi import FastAPI, Depends, status, HTTPException, Response, Request
from typing import Optional, Annotated

from sqlalchemy.exc import IntegrityError, DBAPIError
from sqlalchemy.orm import Session
from sqlalchemy import inspect, Inspector

from . import models, schemas
from .database import engine,  get_db
from . import utilss
from .routers import posts_router, users_router

# App instance
app = FastAPI()
app.include_router(posts_router.router)
app.include_router(users_router.router)

# From the corresponding mapped classes, creates the tables in DB 
schemas.Base.metadata.create_all(bind = engine)

# # GET request to return all records in the Post table
# @app.get('/posts',tags=['Posts'])# , response_model=list[models.ShowPost])
# def get_all_posts(db : Session = Depends(get_db)): 
#     posts = db.query(schemas.Post).all()
#     return posts

# # Get request to return a specfic record based on id
# @app.get('/posts/{post_id}',tags=['Posts'] ,name = 'Get post by id', response_model=models.ShowPost)
# def get_post(post_id: int, db : Session = Depends(get_db)):
#     post = db.query(schemas.Post).filter(schemas.Post.id == post_id).first()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id : {post_id} not found')
#     return post

# # POST request to create a new record of post in the Post table
# # uses PostCreate as request body structure, Depends returns a pydantic object
# @app.post('/posts',tags=['Posts'] , status_code=status.HTTP_201_CREATED, response_model= models.ShowPost)
# def create_post(request : models.PostCreate, db :Session = Depends(get_db)):
#     new_post = schemas.Post(**request.model_dump(), owner_id = 1)
#     db.add(new_post)
#     db.commit()
#     # after commiting, the variable new_post is 'expired', so we refresh, 
#     # retrieve the commited record back to variable
#     db.refresh(new_post)
#     return new_post



# @app.delete('/posts/{post_id}',tags=['Posts'] , status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(post_id : int , db : Session = Depends(get_db)):
#     post_query = db.query(schemas.Post).filter(schemas.Post.id == post_id)
#     post = post_query.first()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id : {post_id} not found')
#     num_rows = post_query.delete(synchronize_session=False)
#     print(f'Deleted {num_rows} rows from {post.__tablename__.upper()} table')
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
    
# @app.put('/posts/{post_id}', tags=['Posts'] , status_code=status.HTTP_202_ACCEPTED, response_model=models.ShowPost)
# def update_post(post_id : int, request : models.PostCreate, db : Session = Depends(get_db)):
#     # updated_post = schemas.Post(request.model_dump(exclude_unset=True))
#     post_query = db.query(schemas.Post).filter(schemas.Post.id == post_id)
#     post = post_query.first()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id : {post_id} not found')
#     num_rows = post_query.update(request.model_dump(exclude_unset=True), synchronize_session=False)
#     print(f'Deleted {num_rows} rows')
#     # post = post_query.first()
#     db.commit()
#     # refreshes the in-memory state of object to match database
#     db.refresh(post)
#     return post


# @app.post('/users', tags = ['Users'],  status_code=status.HTTP_201_CREATED, response_model=models.UserBase)
# def create_user(request : models.UserCreate, db : Session = Depends(get_db)):
#     request.password = utils.hash_password(request.password)
#     new_user = schemas.User(**request.model_dump())
#     try:
#         db.add(new_user)
#         db.commit()
#         db.refresh(new_user)
#     except IntegrityError as e:
#         error_column = utils.get_column_query_constraint_failure(e)
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f'This {error_column} already exists, please select a new {error_column} ')

#     return new_user


# @app.get('/users/{user_id}', tags = ['Users'], name = 'Get user by id', response_model=models.UserBase)
# def get_user(user_id : int , db : Session = Depends(get_db)):
#     return utils.get_user_by_id(user_id, db )
#     # user = db.query(schemas.User).filter(schemas.User.user_id == user_id).first()
#     # if not user:
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'User with user_id : {user_id} not found')
#     # return user


# @app.get('/users/', tags = ['Users'],name='Get User by email or username')# , response_model = models.UserBase
# def get_user_by_username_email(username : str | None = None
#                                , email : str | None = None 
#                                , db : Session = Depends(get_db)):
#     if not username and not email:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Either a 'username' or 'email' must be provided")
#     if username and email:
#         return utils.get_user_by_email_and_username(email , username, db)
#     if username:
#         return utils.get_user_by_username(username, db)
#     if email:
#         return utils.get_user_by_email(email, db)
   
# @app.get('/users', tags = ['Users'],)#, response_model=list[models.UserBase])
# def get_all_users(db : Session = Depends(get_db)):
#     users = db.query(schemas.User).all()
#     return users

# @app.delete('/users/{id}', tags = ['Users'],)
# def delete_user(id : int, db : Session = Depends(get_db)):
#     user_query = db.query(schemas.User).filter(schemas.User.user_id == id)
#     user = user_query.first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'User with user_id : {id} not found')
    
#     num_rows = user_query.delete(synchronize_session=False)
#     print(f'Deleted {num_rows} rows from {user.__tablename__.upper()} table')
#     db.commit()

# @app.put('/users/{user_id}', tags=['Posts'] , status_code=status.HTTP_202_ACCEPTED, response_model=models.ShowPost)
# def update_post(user_id : int, request : models.UserBase, db : Session = Depends(get_db)):
#     # updated_post = schemas.Post(request.model_dump(exclude_unset=True))
#     user_query = db.query(schemas.User).filter(schemas.User.user_id == user_id)
#     user = user_query.first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id : {user_id} not found')
#     num_rows = user_query.update(request.model_dump(exclude_unset=True), synchronize_session=False)
#     print(f'Deleted {num_rows} rows')
#     # post = post_query.first()
#     db.commit()
#     # refreshes the in-memory state of object to match database
#     db.refresh(user)
#     return user