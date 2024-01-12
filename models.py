from pydantic import BaseModel, UUID4, Field
from sqlalchemy import Uuid

class PostCreate(BaseModel):
                            # Model for the request body when CREATING or  UPDATING  a post
    title : str
    content : str
    published : bool | None = False

class ShowPost(PostCreate):
                            # Model for READING a post or returned structure after CREATING or UPDATING a post
    # post_id : int = Field(alias='id')
    created_at : str
