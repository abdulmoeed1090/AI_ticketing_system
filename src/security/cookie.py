from fastapi import Response
from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
)

REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")
)


def set_auth_cookies(
    response: Response,
    access_token: str,
    refresh_token: str
):

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,          # True in production
        samesite="Lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )


def clear_auth_cookies(
    response: Response
):

    response.delete_cookie("access_token")

    response.delete_cookie("refresh_token")