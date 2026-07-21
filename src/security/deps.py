from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.security.jwt_handler import decode_token


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(token: str = Depends(oauth2_scheme)):

    try:

        payload = decode_token(token)

        return payload

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )


def require_roles(*roles):

    def checker(
        current_user=Depends(get_current_user)
    ):

        if current_user["role"] not in roles:

            raise HTTPException(
                status_code=403,
                detail="Access Denied"
            )

        return current_user

    return checker