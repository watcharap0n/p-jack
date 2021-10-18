from pydantic import BaseModel, Field
from typing import Optional, List


class User(BaseModel):
    id: Optional[str] = Field(None, example='id query (String)')
    name: Optional[str] = Field(None, example='name (String')


class Users(BaseModel):
    users: List[User] = Field(None, example='object in array')

