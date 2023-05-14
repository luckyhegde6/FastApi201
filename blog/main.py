from turtle import title
from urllib import response
from fastapi import Depends, FastAPI, HTTPException, status, Response
from sqlalchemy.orm import Session
from datetime import datetime
from passlib.context import CryptContext
from . import  models, schemas
from .database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(engine)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post('/blog', status_code=status.HTTP_201_CREATED, tags= ['blog'])
def create(req: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=req.title, body=req.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags= ['blog'])
def update(id, req: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).update({'title':req.body.title}, 
                                                                  synchronize_session=False)
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f"Blog with id - {id} not available")
    db.commit()
    db.refresh(blog)
    return {'detail': f"Updated the blog with id - {id}- title {req.body.title}"}

@app.delete('/blog', status_code=status.HTTP_204_NO_CONTENT, tags= ['blog'])
def delete(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f"Blog with id - {id} not available")
    blog.delete(synchronize_session=False)
    db.commit()
    db.refresh(blog)
    return {'detail': f"Deleted the blog with id - {id}"}

@app.get('/blog', status_code=200, response_model=schemas.ShowBlog, tags= ['blog'])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=200, tags= ['blog'])
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f"Blog with id - {id} not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"Blog with id - {id} not available"}
    return blog

@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, tags= ['users'])
def create_user(req: schemas.User, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(req.password)
    user = db.query(models.User).filter(models.User.username == req.username).first()
    if user:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,
                            detail= f"User with username - {req.username} already exists")
    new_user = models.User(email=req.email, password=hashed_password, username=req.username, created_at=datetime.now())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/users/{username}', status_code=200, response_model=schemas.ShowUser, tags= ['users'])
def showuser(username, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f"User with username - {username} not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"Blog with id - {id} not available"}
    return user

@app.put('/users/{username}', status_code=status.HTTP_202_ACCEPTED, tags= ['users'])
def update_useremail(username, req: schemas.User, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).update({'email':req.email}, 
                                                                  synchronize_session=False)
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f"User with username - {username} not available")
    db.commit()
    db.refresh(user)
    return {'detail': f"Updated the user with username - {username}- email {req.email}"}

@app.delete('/users', status_code=status.HTTP_204_NO_CONTENT, tags= ['users'])
def delete_user(username, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username)
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f"User with username - {username} not available")
    user.delete(synchronize_session=False)
    db.commit()
    db.refresh(user)
    return {'detail': f"Deleted the user with username - {username}"}