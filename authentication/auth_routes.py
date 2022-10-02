from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from database.db import get_db
from sqlalchemy.orm.session import Session
from database.models import DbUser
from database.hasher import Hash
from authentication.auth import create_access_token

router = APIRouter(
  tags=['authentication']
)

hasher = Hash()

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
  expt = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='error logging in')

  user: DbUser = db.query(DbUser).filter(DbUser.username == request.username).first()
  if not user:
    raise expt
  
  verified = hasher.verify(user.password, request.password)

  if not verified:
    raise expt

  access_token = create_access_token({'username': user.username})

  return {
    'access_token': access_token,
    'token_type': 'bearer',
    'user_id': user.id,
    'username': user.username
  }