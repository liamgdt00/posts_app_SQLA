from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt, ExpiredSignatureError

from sqlalchemy.orm import Session

from typing import Annotated

from . import schemas , models, database
from .utilss import usersq
from .config import settings
from datetime import datetime, timedelta, timezone


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET KEY -> Only visibile on backend for generaring unique, tamper proof token
# ALGORITHM -> hashing algorithm for token
# EXPIRATION TIME -> default expiration time for token

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
TOKEN_EXPIRES_MINUTES = settings.access_token_expires_minutes

def create_access_token(data : dict):
    # copy the data to encode inorder to not modify the mutable dictionary
    to_encode = data.copy()
    #set the expiry time 
    expires_in = datetime.now(timezone.utc) + timedelta(minutes = TOKEN_EXPIRES_MINUTES)
    # update the data to encode with an expiry time
    to_encode.update({'exp' : expires_in})
    # encode the data via jwt, using the data to encode, signing SECRET, and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    # run a correct user through login route, can check jwt token via jwt.io
    return encoded_jwt


def verify_access_token(token : str , credentials_exception):
    try:
        # decode jwt token via same SECRET and algorithm, and extract the useful information
        payload : dict = jwt.decode(token, SECRET_KEY , algorithms=[ALGORITHM])
        expiry_time = payload.get('exp')
        if expiry_time < datetime.timestamp(datetime.now()):
            raise HTTPException(status_code=440, detail = f'Login timeout')
        user_id : str = payload.get('users_id')
        if not user_id:
            raise credentials_exception
        
        # store data as a pydantic model ( not necessary but good practice)
        token_data = models.TokenData(id = user_id)
    except JWTError as jwte:
        if isinstance(jwte, ExpiredSignatureError):
            print('Signature has expired')
            raise HTTPException(status_code=440, detail = f'Login timeout')
        
        raise credentials_exception
    # return the required data
    
    return token_data

def get_current_user_id(token : Annotated[str, Depends(oauth2_scheme),
                     'Extracts current user_id from a request, have to be logged in ( have token) to post'],
                     db : Session = Depends(database.get_db)):
    # custom exception for the verify_access_token() function
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail = f'Could nottt validate credentials',
                                          headers={"WWW-Authenticate": "Bearer"})
    
    token_data = verify_access_token(token , credentials_exception)

    user = usersq.query_user_by_id(token_data.id , db).first()
    print(f'**************************************\n\nuser = {user}\n\n type = {type(user)}')
    return token_data