from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from .. import schemas, models

def get_post_query_by_id(post_id : int , db : Session):
    '''
    Utility query to retrieve the post record corresponding to the provided id

    Uses FastAPI Error handling in the case of no matching record
    
    Input:
    post_id = integer id for a particular post
    db = Session object to interact with the database
    
    Returns:
    post_query = the records returned corresponding to a post with id = post_id
        - expected behaviour is only one post is returned'''
    
    post_query = db.query(schemas.Post).filter(schemas.Post.id == post_id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Post with id : {post_id} not found')
    return post_query

def create_post(request : models.PostCreate, db :Session , owner_id : int):
    new_post = schemas.Post(**request.model_dump(), owner_id = owner_id)
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