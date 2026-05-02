#py -m pip install fastapi uvicorn

#py -m pip install "fastapi[all]"

from fastapi import FastAPI, status

app = FastAPI()

@app.get("/")
def index():
    """
    This is the index page of our FastAPI application.
    """
    return {"message": "FastApi instalation complete!"}

@app.post("/user", status_code=status.HTTP_201_CREATED)
def make_account():

    
    return {"status":201, "message": "Created", "user": {"username": "John Doe"}}

@app.get("/user/{user_id}")
def info(id:str):
    return {"user_id": id, }
