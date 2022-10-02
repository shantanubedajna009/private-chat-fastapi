import datetime
from schemas import UserRequest
from database.models import DbUser
from sqlalchemy.orm.session import Session
from database.hasher import Hash

hasher = Hash()

def create_user(request: UserRequest, db: Session):
    new_user = DbUser(
        username        = request.username,
        email           = request.email,
        password        = hasher.bcrypt(request.password),
        date_created    = datetime.datetime.now()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user