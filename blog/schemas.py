from typing import List 
import datetime
from sqlite3 import Date
from typing import Optional, Union
from pydantic import BaseModel

class BlogBase(BaseModel):
    title: str
    body:str
    published: Optional [bool]

class Blog(BlogBase):
    title: str
    body:str
    published: Optional [bool]
    class Config:
        orm_mode = True

class User(BaseModel):
    email: str
    password:str
    username: str
    created_at:Optional [Date]

class Login(BaseModel):
     username: str
     password: str

class ShowUser(User):
    email: str
    username: str
    blogs: List[Blog]

    class Config:
        orm_mode = True

class ShowBlog(Blog) : 
        title: str
        body: str
        creator: ShowUser
        
        class Config:
             orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str]= None
