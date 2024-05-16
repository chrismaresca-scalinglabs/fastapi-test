import os
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import requests
from app.auth import User
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve environment variables
COGNITO_REGION = os.getenv("COGNITO_REGION")
COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
COGNITO_APP_CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID")

if not all([COGNITO_REGION, COGNITO_USER_POOL_ID, COGNITO_APP_CLIENT_ID]):
    raise Exception("Missing one or more environment variables for Cognito configuration")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_jwks():
    url = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}/.well-known/jwks.json"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    jwks = get_jwks()
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    if rsa_key:
        try:
            payload = jwt.decode(token,
                                 rsa_key,
                                 algorithms=["RS256"],
                                 audience=COGNITO_APP_CLIENT_ID)

            print(payload)

            email = payload.get("username")
            if email is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return User(email=email)
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
    raise HTTPException(status_code=401, detail="Invalid token")
