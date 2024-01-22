from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError
from passlib.context import CryptContext

from .. import schemas, models

def get_post_query_by_id(post_id : int , db : Session):
    post_query = db.query(schemas.Post).filter(schemas.Post.id == post_id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Post with id : {post_id} not found')
    return post_query

def create_post(request : models.PostCreate, db :Session):
    new_post = schemas.Post(**request.model_dump(), owner_id = 1)
    db.add(new_post)
    db.commit()
    # after commiting, the variable new_post is 'expired', so we refresh, 
    # retrieve the commited record back to variable
    db.refresh(new_post)
    return new_post

def query_posts_containing_string( string : str , db : Session):
    search_pattern = f'%{string}%'
    titles_query = db.query(schemas.Post).filter(schemas.Post.title.like(search_pattern))
    if not titles_query.all():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail = f'No posts containing {string} in the title were found')
    return titles_query