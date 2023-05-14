import datetime
from sqlite3 import Date
from typing import Optional, Union
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body:str
    published: Optional [bool]

class User(BaseModel):
    email: str
    password:str
    username: str
    created_at:Optional [Date]

class ShowUser(User):
    email: str
    username: str

    class Config:
        orm_mode = True

class ShowBlog(Blog) : 
        title: str
        body: str
        creator: ShowUser
        
        class Config:
             orm_mode = True
