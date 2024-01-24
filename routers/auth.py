from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from typing import Annotated

from .. import database, models, schemas
from .. utilss import utils
from ..oauth2 import create_access_token

router = APIRouter(tags = ['Authentication'])

@router.post('/login', response_model=models.Token)
def login_for_token(login_credentials :Annotated [OAuth2PasswordRequestForm,
                                                    Depends(),
                                                    'Can provide either a valid username or email'], 
                    db : Session = Depends(database.get_db)
                    ) -> Annotated[models.Token, 'return token for JWT authentication']:
    # Search for user in db, handle any errors
    user = db.query(schemas.User).filter((schemas.User.username == login_credentials.username)
                                         | (schemas.User.email == login_credentials.username)).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                 detail = f'Invalid credentials.')
            
    if not utils.verify_password(login_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid credentials.')
    
    # create JWT access token with data to encode into token payload (retrieved later)
    # can include other data such as scope, roles, other data etc...
    print(f'User_id = {user.user_id}\nType user_id = {type(user.user_id)}')
    access_token = create_access_token(data = {'users_id' : user.user_id})

    return models.Token(access_token=access_token, token_type='bearer')