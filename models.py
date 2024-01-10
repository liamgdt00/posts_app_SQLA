from pydantic import BaseModel, UUID4
from sqlalchemy import Uuid

class PostCreate(BaseModel):
    title : str
    content : str
    published : bool | None = False

class Post(PostCreate):
    post_id : str
    created_at : str
