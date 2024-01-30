
from fastapi import HTTPException, status

from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import schemas

# USER RELATED QUERIES

def query_user_by_id(id : int, db : Session):
    user_query = db.query(schemas.User).filter(schemas.User.user_id == id)
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail = f"User with the id : {id} not found")
    return user_query

def query_user_by_username(username :str , db : Session):
    user_query = db.query(schemas.User).filter(func.lower(schemas.User.username) == username.lower())
    if not user_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail = f"User with the username : {username} not found")
    return user_query

def query_user_by_email(email :str , db : Session):
    user_query = db.query(schemas.User).filter(func.lower(schemas.User.email) == email.lower())
    if not user_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail = f"User with the email : {email} not found")
    return user_query

def query_user_by_email_and_username(email : str , username : str, db : Session):
    user_query = db.query(schemas.User).filter((func.lower(schemas.User.username) == username.lower()) 
                                               & (func.lower(schemas.User.email) == email.lower()))
    if not user_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail = f"User with the email : {email} and username : {username} not found")
    return user_query
