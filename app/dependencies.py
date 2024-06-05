from typing import Optional

# FastAPI
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Response

# Import roles
from app.roles import ROLE_HIERARCHY

# Firebase
from firebase_admin import auth, credentials, initialize_app


credential = credentials.Certificate(cert='key.json')
initialize_app(credential=credential)



def get_current_user(required_role: Optional[str] = None):
    async def _get_current_user(
        res: Response, credential: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))
    ):
        if credential is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Bearer authentication is needed",
                headers={'WWW-Authenticate': 'Bearer realm="auth_required"'},
            )
        try:
            decoded_token = auth.verify_id_token(credential.credentials)
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid authentication from Firebase. {err}",
                headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
            )
        
        res.headers['WWW-Authenticate'] = 'Bearer realm="auth_required"'

        user_role = decoded_token.get('role')

        # Check role hierarchy
        if required_role:
            user_role_level = ROLE_HIERARCHY.get(user_role, 0)
            required_role_level = ROLE_HIERARCHY.get(required_role, 0)
            if user_role_level < required_role_level:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"User does not have the required role: {required_role}",
                )

        return decoded_token

    return _get_current_user


