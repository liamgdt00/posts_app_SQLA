from fastapi import FastAPI, Depends, status, HTTPException
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
    new_post = schemas.Post(title = request.title, content = request.content, published = request.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get('/posts')
def get_posts(db : Session = Depends(get_db)):
    posts = db.query(schemas.Post).all()
    return posts
    
@app.get('/posts/{uuid_string}')
def get_post(uuid_string : str, db : Session = Depends(get_db)):
    post = db.query(schemas.Post).filter(schemas.Post.id == uuid_string).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id : {uuid_string} not found')
    return post
    

