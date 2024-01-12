from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# URL for connecting to the database ---> can be added to config / .env file at some point
SQLITE_DATABASE_URL = 'sqlite:///./blog.db'

# engine instance for db connection
engine = create_engine(SQLITE_DATABASE_URL, connect_args={
                       "check_same_thread": False})

# SessionLocal class to be imported for creating connecitons to db
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

# Used to register python classes as valid database tables, and track metadata
# table classes inherit from Base, signalling to SQLalchemy ORM that these should be mapped as tables in the DB
Base = declarative_base()