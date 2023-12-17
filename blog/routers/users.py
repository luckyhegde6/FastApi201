from typing import List
from fastapi import APIRouter, FastAPI, Request, Response, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from passlib.context import CryptContext
from .. import  models, schemas
from ..database import engine, SessionLocal

router= APIRouter(
     prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(engine)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
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

@router.get('/{username}', status_code=200, response_model=schemas.ShowUser)
def showuser(username, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f"User with username - {username} not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"Blog with id - {id} not available"}
    return user

@router.put('/{username}', status_code=status.HTTP_202_ACCEPTED)
def update_useremail(username, req: schemas.User, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).update({'email':req.email}, 
                                                                  synchronize_session=False)
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f"User with username - {username} not available")
    db.commit()
    db.refresh(user)
    return {'detail': f"Updated the user with username - {username}- email {req.email}"}

@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(username, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username)
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f"User with username - {username} not available")
    user.delete(synchronize_session=False)
    db.commit()
    db.refresh(user)
    return {'detail': f"Deleted the user with username - {username}"}