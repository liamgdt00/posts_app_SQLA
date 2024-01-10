from .database import Base
from sqlalchemy import Column, Integer, Uuid, String, Table, Boolean
import uuid
from datetime import datetime

class Post(Base):
    __tablename__ = 'posts'
    id = Column(String, primary_key=True, default = lambda : str(uuid.uuid4()))
    title = Column(String)
    content = Column(String)
    published = Column(Boolean , default = False)
    created_at = Column(String, default = datetime.now)
    