from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError
from passlib.context import CryptContext

from . import schemas, models

# USER RELATED QUERIES

def get_user_by_id(id : int, db : Session):
    user = db.query(schemas.Users).filter(schemas.Users.user_id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail = f"User with the id : {id} not found")
    return user

def get_user_by_username(username :str , db : Session):
    user = db.query(schemas.Users).filter(schemas.Users.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail = f"User with the username : {username} not found")
    return user

def get_user_by_email(email :str , db : Session):
    user = db.query(schemas.Users).filter(schemas.Users.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail = f"User with the email : {email} not found")
    return user

def get_user_by_email_and_username(email : str , username : str, db : Session):
    user = db.query(schemas.Users).filter((schemas.Users.username == username) & (schemas.Users.email == email)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail = f"User with the email : {email} and username : {username} not found")
    return user

# POST RELATED QUERIES


pwd_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')



def get_column_query_constraint_failure(error) -> str:
    error = str(error.orig)
    table_dot_column = error.split(': ')[-1]
    column = table_dot_column.split('.')[-1]
    return column

def hash_password(raw_pwd : str) -> str:
    return pwd_context.hash(raw_pwd)

def verify_password(raw_pwd : str, hashed_pwd : str) -> bool:
    return pwd_context.verify(raw_pwd, hashed_pwd)
