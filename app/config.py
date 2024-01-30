from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_provider : str
    database_hostname : str | None
    database_port : str | None
    database_password : str | None
    database_name : str
    database_username : str | None
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int
    pass 

settings = Settings()



