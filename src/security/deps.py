from fastapi import Depends, HTTPException, Request
from src.security.jwt_handler import decode_token


def get_current_user(request: Request):

    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    try:
        payload = decode_token(token)

        if payload.get("type") != "access":
            raise HTTPException(
                status_code=401,
                detail="Invalid access token"
            )

        return payload

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


def require_roles(*roles):

    def checker(current_user=Depends(get_current_user)):

        if current_user["role"] not in roles:
            raise HTTPException(
                status_code=403,
                detail="Access Denied"
            )

        return current_user

    return checker