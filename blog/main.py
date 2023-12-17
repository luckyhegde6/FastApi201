from fastapi import  FastAPI, HTTPException
from .routers import blogs, users, auth

app = FastAPI()
app.include_router(auth.router)
app.include_router(blogs.router)
app.include_router(users.router)
