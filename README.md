# FastApi201

fastApi advanced

# Windows

# You can also use `py -3 -m venv .venv`

`python -m venv .venv`
refer - `https://docs.python.org/3/tutorial/venv.html` for more on virtual env

## Activating venv on Windows

`.venv\Scripts\activate.bat`

## for installing on windows

`python -m pip install fastapi`

## for installation of server

`pip install uvicorn`

## For listing and freezing requirements

`python -m pip list`
`python -m pip freeze > requirements.txt`

## To install from requirements text

`python -m pip install -r requirements.txt`

## for checking the initialize

`python myapi.py`

## for running the server

`uvicorn myapi:app --reload`

## for running the blog  server

`uvicorn blog.main:app --reload`

- for swagger UI page  `http://127.0.0.1:8000/docs`
- for redoc swagger page  `http://127.0.0.1:8000/redoc`
