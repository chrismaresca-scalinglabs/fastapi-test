from fastapi import FastAPI, Depends, HTTPException
from app.dependencies import get_current_user, get_user_token
from app.auth import User


app = FastAPI()

@app.get("/public")
def read_public():
    return {"message": "This is a public endpoint"}

@app.get("/protected")
def read_protected(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.email}! This is a protected endpoint"}

@app.get("/protected2")
def read_protected(current_user: User = Depends(get_user_token)):
    return {"msg":"Hello, user","uid":current_user['uid']} 
