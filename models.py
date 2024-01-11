from pydantic import BaseModel, UUID4, Field
from sqlalchemy import Uuid

class PostCreate(BaseModel):
    title : str
    content : str
    published : bool | None = False

class ShowPost(PostCreate):
    # post_id : int = Field(alias='id')
    created_at : str
