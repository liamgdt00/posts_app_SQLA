from fastapi import APIRouter, Response, status, HTTPException, Depends

from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import database, schemas, models, oauth2
from ..utilss import postsq

router = APIRouter(
    tags=['Posts'],
    prefix='/posts'
)

# GET request to return all records in the Post table
@router.get('/' , response_model=list[models.PostShow], response_model_by_alias=False)
def get_all_posts(db : Session = Depends(database.get_db)):
    posts = db.query(schemas.Post).all()
    return posts


# Get request to return a specfic record based on id
@router.get('/{post_id}' ,name = 'Get post by id',
             response_model=models.PostShow, response_model_by_alias=False)
def get_post(post_id: int, db : Session = Depends(database.get_db)):
    post_query = postsq.get_post_query_by_id(post_id, db)
    post = post_query.first()
    return post


# POST request to create a new record of post in the Post table
# uses PostCreate as request body structure, Depends returns a pydantic object
@router.post('/' , status_code=status.HTTP_201_CREATED,
              response_model= models.PostShow, response_model_by_alias=False)
def create_post(request : models.PostCreate, db :Session = Depends(database.get_db),
                current_user : models.TokenData = Depends(oauth2.get_current_user_id)):
    return postsq.create_post(request, db , current_user.id)


@router.delete('/{post_id}' , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id : int ,
                db : Session = Depends(database.get_db),
                current_user : models.TokenData = Depends(oauth2.get_current_user_id)):
    
    post_query = postsq.get_post_query_by_id(post_id , db)
    post = post_query.first()

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail= f'Not authroised to perform the requested action')
    
    table_name = post.__tablename__
    num_rows = post_query.delete(synchronize_session=False)
    print(f'Deleted {num_rows} rows from {table_name.upper()} table')
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put('/{post_id}' , status_code=status.HTTP_202_ACCEPTED,
             response_model=models.PostShow, response_model_by_alias=False)
def update_post(post_id : int, request : models.PostCreate,
                db : Session = Depends(database.get_db),
                current_user : models.TokenData = Depends(oauth2.get_current_user_id)):
    
    post_query = postsq.get_post_query_by_id(post_id , db)
    post = post_query.first()

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail= f'Not authroised to perform the requested action')
    
    table_name = post.__tablename__
    num_rows = post_query.update(request.model_dump(exclude_unset=True), synchronize_session=False)
    print(f'Updated {num_rows} rows from the {table_name.upper()} table.')
    db.commit()
    # refreshes the in-memory state of object to match database
    db.refresh(post)
    return post

@router.get('/title/{title_pattern}', response_model=list[models.PostShow])
def get_title_containig_pattern(title_pattern : str , db : Session = Depends(database.get_db)):
    titles_query = postsq.query_posts_containing_string(title_pattern, db)
    return titles_query.all()
