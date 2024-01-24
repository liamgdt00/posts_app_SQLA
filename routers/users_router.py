from fastapi import APIRouter, Response, status, HTTPException, Depends

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .. import database, schemas, models
from ..utilss import usersq, utils

router = APIRouter(
    tags = ['Users']
)

@router.post('/users',   status_code=status.HTTP_201_CREATED, response_model=models.UserBase)
def create_user(request : models.UserCreate, db : Session = Depends(database.get_db)):
    '''
    Create a user with all the following information:
    - **username**: a unique username
    - **email**:  a valid, unique email
    - **password**: a secure password
    '''
    request.password = utils.hash_password(request.password)
    new_user = schemas.User(**request.model_dump())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError as e:
        error_column = utils.get_column_query_constraint_failure(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f'This {error_column} already exists, please select a new {error_column} ')

    return new_user


@router.get('/users/{user_id}',  name = 'Get user by id', response_model=models.UserBase)
def get_user(user_id : int , db : Session = Depends(database.get_db)):
    user_query = usersq.query_user_by_id(user_id, db )
    return user_query.first()


@router.get('/users/', name='Get User by email or username')# , response_model = models.UserBase
def get_user_by_username_email(username : str | None = None
                               , email : str | None = None 
                               , db : Session = Depends(database.get_db)):
    if not username and not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Either a 'username' or 'email' must be provided")
    if username and email:
        return usersq.query_user_by_email_and_username(email , username, db).first()
    if username:
        return usersq.query_user_by_username(username, db).first()
    if email:
        return usersq.query_user_by_email(email, db).first()
   
@router.get('/users', )#, response_model=list[models.UserBase])
def get_all_users(db : Session = Depends(database.get_db)):
    users = db.query(schemas.User).all()
    return users

@router.delete('/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id : int, db : Session = Depends(database.get_db)):
    user_query = usersq.query_user_by_id(user_id , db)
    table_name = user_query.first().__tablename__
    num_user_rows = user_query.delete(synchronize_session=False)
    print(f'Deleted {num_user_rows} rows from {table_name.upper()} table')
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/users/{user_id}' , status_code=status.HTTP_202_ACCEPTED, response_model=models.UserShow)
def update_user(user_id : int, request : models.UserBase, db : Session = Depends(database.get_db)):
    user_query = usersq.query_user_by_id(user_id, db)
    user = user_query.first()
    table_name = user.__tablename__
    num_rows = user_query.update(request.model_dump(exclude_unset=True), synchronize_session=False)
    print(f'Updated {num_rows} rows from the {table_name} table.')
    db.commit()
    # refreshes the in-memory state of object to match database
    db.refresh(user)
    return user
