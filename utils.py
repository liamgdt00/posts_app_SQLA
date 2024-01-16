from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError
from . import schemas

# def user_exists(db : Session, username : str = None, email : str = None):
#     query =  db.query(schemas.Users).filter((schemas.Users.username == username) | schemas.Users.email == email)
#     result = query.all()
#     return result


def get_column_query_constraint_failure(error):
    error = str(error.orig)
    table_dot_column = error.split(': ')[-1]
    column = table_dot_column.split('.')[-1]
    return column