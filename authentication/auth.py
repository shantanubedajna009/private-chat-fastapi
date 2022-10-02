from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import timedelta, datetime
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm.session import Session
from database.db import get_db
from database.models import DbUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY = '333809dfe79d55fc49216952965632e7cc0b46b1d27ce34792581014a6cef1b1'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()

  if expires_delta:
    expires = datetime.utcnow() + expires_delta
  else:
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  
  to_encode.update({'exp': expires})

  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

  return encoded_jwt

def get_current_user_from_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},)
  
  try:
    data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = data.get('username', None)
    if not username:
      raise credentials_exception
  except JWTError:
    raise credentials_exception

  user = db.query(DbUser).filter(DbUser.username == username).first()
  if not user:
    raise credentials_exception

  return user

