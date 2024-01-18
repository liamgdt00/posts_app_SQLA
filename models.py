from pydantic import BaseModel, UUID4, Field
from sqlalchemy import Uuid
from typing import Annotated
from datetime import datetime
class PostCreate(BaseModel):
                            # Model for the request body when CREATING or  UPDATING  a post
    title : str
    content : str
    published : bool | None = False

class ShowPost(PostCreate):
                            # Model for READING a post or returned structure after CREATING or UPDATING a post
    # post_id : int = Field(alias='id')
    created_at : datetime
    owner_id : int


class UserBase(BaseModel):
    username : str
    email : str
    # username : Annotated[ str , Field(pattern = r'')]

class UserShow(UserBase):
    created_at : str
class UserCreate(UserBase):
    password : str

class Profile(UserBase):
    first_name : str
    last_name : str
    account_no : int
