from .database import Base
from sqlalchemy import Column, Integer, Uuid, String, Table, Boolean
import uuid
from datetime import datetime

class Posts(Base):
    # ORM table structure for the posts table
    # Use 'server_default' to force the db server to control / send the defualt, rather than client / python
    # Not aplpicable to sqlite as it is in memory db

    __tablename__ = 'posts'
    # id = Column(String, primary_key=True, default = lambda : str(uuid.uuid4()))
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean , default = False, nullable=False)
    created_at = Column(String, default = datetime.now, nullable=False)
    
class Users(Base):

    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
