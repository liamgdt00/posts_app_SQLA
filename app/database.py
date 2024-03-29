from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import settings

# URL for connecting to the database ---> can be added to config / .env file at some point
SQLITE_DATABASE_URL = f'{settings.database_provider}:///./{settings.database_name}'

# dialect+driver://username:password@host:port/database
# without dialect = postgresql://user:password@postgresserver/db
# with dialect = postgresql+psycopg2://scott:tiger@localhost:5432/mydatabase

# engine instance for db connection
engine = create_engine(SQLITE_DATABASE_URL, connect_args={
                       "check_same_thread": False},echo=True)

# SessionLocal class to be imported for creating connecitons to db
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Used to register python classes as valid database tables, and track metadata
# table classes inherit from Base, signalling to SQLalchemy ORM that these should be mapped as tables in the DB
Base = declarative_base()

# Yields an independent session / conneciton to db, and maintains state/ connection until request finished/ fails
def get_db():       # Function to return a db
    db = SessionLocal()
    # sqlite oddity where foreign keys are not enforced implcitly
    db.execute(text("PRAGMA foreign_keys=ON"))
    try:
        yield db
        print('Successfully connected to db')
    except Exception as e:
        print(f'Error : {e}')
        print('Trouble connecting to database')
    finally:
        db.close()

from . import schemas


