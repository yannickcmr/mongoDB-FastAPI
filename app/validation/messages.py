from pydantic import BaseModel, Field
from typing import Optional, Any


""" Request Validation Classes """

class DBGetUser(BaseModel):
    """ BaseModel for gathering User from the Database. """
    userID: Optional[int]
    email: Optional[str]
    phone: Optional[str]

class DBAddUser(BaseModel):
    """ BaseModel for adding a new User to the Database. """
    name: str
    email: str
    phone: Optional[str] = Field(..., min_length=6, max_length=16)
    birthday: Optional[str] = Field(..., description="Use format 'DD-MM-YYYY")
    address: Optional[dict] = Field(..., description="Use pattern: {'street': "", 'city': "", 'postal': "", 'country': ""}")

class DBDeleteUser(BaseModel):
    """ BaseModel for deleting an existing User from the Database. """
    userID: Optional[int]
    email: Optional[str]
    phone: Optional[str]


""" Response Validation Classes """

class MessageResponse(BaseModel):
    """ BaseModel for a default Message Response. """
    msg: str
    code: int
    data: Optional[dict] = None

class DataResponse(BaseModel):
    """ BaseModel for a default Data Response. """
    msg: str
    code: int
    data: dict

    def check_data(self) -> None:
        pass

class ErrorResponse(BaseModel):
    msg: str
    code: int = 400
    data: None = None
