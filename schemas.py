import datetime
from typing import List
from pydantic import BaseModel
from enum import Enum

####### Reveiver Schemas ############################

class UserRequest(BaseModel):
    username: str
    email: str
    password: str

class UserAuth(BaseModel):
  id: int
  username: str
  email: str


######## Receiver Schemas ends here #################

############ Display Schemas ########################

class UserDisplay(BaseModel):
    username: str
    email: str
    date_created: datetime.datetime

    class Config():
        orm_mode = True

########### Display Schemas ends here ###############