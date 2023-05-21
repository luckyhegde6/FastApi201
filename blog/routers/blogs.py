from typing import List
from fastapi import APIRouter, FastAPI, Request, Response, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from passlib.context import CryptContext
from .. import  models, schemas
from ..database import engine, SessionLocal

router= APIRouter(
     prefix="/blog",
    tags=["blog"],
    responses={404: {"description": "Not found"}},
)

models.Base.metadata.create_all(engine)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(req: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=req.title, body=req.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, req: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).update({'title':req.body.title}, 
                                                                  synchronize_session=False)
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f"Blog with id - {id} not available")
    db.commit()
    db.refresh(blog)
    return {'detail': f"Updated the blog with id - {id}- title {req.body.title}"}

@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f"Blog with id - {id} not available")
    blog.delete(synchronize_session=False)
    db.commit()
    db.refresh(blog)
    return {'detail': f"Deleted the blog with id - {id}"}

@router.get('/', status_code=200, response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.get('/{id}', status_code=200, tags= ['blog'])
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f"Blog with id - {id} not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"Blog with id - {id} not available"}
    return blog
