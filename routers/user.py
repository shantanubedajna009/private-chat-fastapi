from fastapi import APIRouter, Depends
from schemas import UserDisplay, UserRequest
from sqlalchemy.orm.session import Session
from database.db import get_db
from database.user_operations import create_user

router = APIRouter(
    prefix='/user',
    tags=['User']
)

@router.post('/new', response_model=UserDisplay)
def api_create_new_user(request: UserRequest, db: Session = Depends(get_db)):
    return create_user(request, db)
