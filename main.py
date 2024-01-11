from fastapi import FastAPI, Depends, status, HTTPException, Response
from . import models, schemas
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

schemas.Base.metadata.create_all(bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
        print('Successfully connected to db')
    except Exception as e:
        print('Trouble connecting to database')
        print(f'Error : {e}')
    finally:
        db.close()

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(request : models.PostCreate, db :Session = Depends(get_db)):
    new_post = schemas.Posts(title = request.title, content = request.content, published = request.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get('/posts')
def get_posts(db : Session = Depends(get_db)):
    posts = db.query(schemas.Posts).all()
    return posts
    
@app.get('/posts/{post_id}')
def get_post(post_id: int, db : Session = Depends(get_db)):
    post = db.query(schemas.Posts).filter(schemas.Posts.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id : {post_id} not found')
    return post

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
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id : {post_id} not found')
    
    post_query.update(request.model_dump(exclude_unset=True))
    post = post_query.first()
    db.commit()
    db.refresh(post)
    return post