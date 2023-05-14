from turtle import title
from typing import Optional, Union
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get('/')
def read_root():
    return {"Hello": "World"}

@app.get('/blog')
#/blog?limit=10&published=true
def index(limit=10, published:bool = True, sort : Optional[str] = None):
    # fetch only 10 published blogs
    if published:
        return {'data': f'{limit } published blogs from the list'}  
    else:
        return {'data': f'{limit } blogs from the list'} 

@app.get('/blog/unpublished')
def unpublished():
    # fetch blog with id =id
    return {'data': 'unpublished blogs'}  

@app.get('/blog/{id}')
def show(id: int):
    # fetch blog with id =id
    return {'data': id}  

@app.get('/blog/{id}/comments')
def comments(id: int):
    # fetch comments of blog with id =id
    return {'data': {'1','2'}}  

class Blog(BaseModel):
    title: str
    body:str
    published: Optional [bool]

@app.post('/blog')
def create_blog(req:Blog):
    # fetch blog with id =id
    return {'data': f'Blog is created with title as {req.title}'} 

if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)