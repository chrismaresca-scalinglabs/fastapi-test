from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Firebase
from firebase_admin import auth, firestore
from firebase_admin.auth import UserRecord
from firebase_admin.exceptions import FirebaseError


# Pydantic
from pydantic import BaseModel

from app.dependencies import get_current_user
from app.roles import ROLE_HIERARCHY


app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/public")
def read_public():
    return {"message": "This is a public endpoint"}

# @app.get("/protected")
# def read_protected(current_user: User = Depends(get_current_user)):
#     return {"message": f"Hello, {current_user.email}! This is a protected endpoint"}


class UpgradeRequest(BaseModel):
    role: str


@app.post("/set-role")
async def set_role(request: UpgradeRequest, current_user: dict = Depends(get_current_user())):
    uid = current_user['uid']

    # Validate the requested role
    if request.role not in ROLE_HIERARCHY.keys():
        raise HTTPException(status_code=400, detail="Invalid role")

    try:
        # Get the current claims to rollback if needed
        user_record: UserRecord = auth.get_user(uid)

        current_claims = user_record.custom_claims if user_record.custom_claims else {}

        # Set custom claims to upgrade the user's role
        auth.set_custom_user_claims(uid, {'role': request.role})

        # Update Firestore document
        db = firestore.client()
        user_ref = db.collection('users').document(uid)
        user_ref.update({'role': request.role})

        return {"message": "Account upgraded successfully. Please refresh your token."}
    except Exception as e:
        # Rollback custom claims if Firestore update fails
        try:
            auth.set_custom_user_claims(uid, current_claims)
        except Exception as rollback_error:
            raise HTTPException(status_code=500, detail=f"Original error: {str(e)}, Rollback error: {str(rollback_error)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/read-user-info")
async def read_info(current_user: dict = Depends(get_current_user(required_role="paid"))):
    return {"message": "Admin info", "user": current_user}

class UserCheckRequest(BaseModel):
    email: str

@app.post("/api/check-user")
async def check_user(request: UserCheckRequest):
    try:
        db = firestore.client()
        users_ref = db.collection('users')
        query = users_ref.where('email', '==', request.email).limit(1)
        results = query.stream()

        user_exists = any(results)

        return {"exists": user_exists}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))