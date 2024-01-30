from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

def get_column_query_constraint_failure(error) -> str:
    error = str(error.orig)
    table_dot_column = error.split(': ')[-1]
    column = table_dot_column.split('.')[-1]
    return column

def hash_password(raw_pwd : str) -> str:
    return pwd_context.hash(raw_pwd)

def verify_password(raw_pwd : str, hashed_pwd : str) -> bool:
    return pwd_context.verify(raw_pwd, hashed_pwd)