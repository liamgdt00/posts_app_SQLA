from fastapi import Body
from pydantic import BaseModel, UUID4, Field, EmailStr, ConfigDict
from sqlalchemy import Uuid
from typing import Annotated, Union, Optional
from datetime import datetime

class PostBase(BaseModel):  # Model for the request body when CREATING or  UPDATING  a post        
    title : str
    content : str
    published : bool | None = False

class UserBase(BaseModel):
    username : str
    email : EmailStr
    # username : Annotated[ str , Field(pattern = r'')]

class UserShow(UserBase):
    created_at : str
    user_id : int
    created_at : datetime
    posts : list[PostBase] = Field(alias='posts_rel')


class UserCreate(UserBase):
    password : str


class UserLogin(BaseModel):
    username_or_email : Union[str, EmailStr]
    password : str


class PostCreate(PostBase):
    pass

class PostShow(PostCreate): # Model for READING a post or returned structure after CREATING or UPDATING a post   
    post_id : int = Field(alias='id')
    created_at : datetime
    owner_id : int
    author : UserBase = Field(alias = 'owner_rel')
    

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id: int | None = None

class Profile(UserBase):
    first_name : str
    last_name : str
    account_no : int

