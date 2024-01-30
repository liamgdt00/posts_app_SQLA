from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')
    database_provider : str
    database_hostname : str | None = None
    database_port : str | None = None
    database_password : str | None = None
    database_name : str
    database_username : str | None = None
    secret_key : str
    algorithm : str
    access_token_expires_minutes : int
    

settings = Settings()



