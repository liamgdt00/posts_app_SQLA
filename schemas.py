from .database import Base
from sqlalchemy import Column, Integer, Uuid, String, Table, Boolean
import uuid
from datetime import datetime

class Posts(Base):
    __tablename__ = 'posts'
    # id = Column(String, primary_key=True, default = lambda : str(uuid.uuid4()))
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean , default = False)
    created_at = Column(String, default = datetime.now)
    