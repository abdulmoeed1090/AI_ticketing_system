from fastapi import APIRouter, Response, Request
from pydantic import BaseModel

from src.services import auth_s as s
from src.security.cookie import set_auth_cookies, clear_auth_cookies
from src.security.deps import get_current_user
from fastapi import Depends

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


class UserSignup(BaseModel):
    name: str
    email: str
    password: str
    role: str


class UserLogin(BaseModel):
    email: str
    password: str


@router.post("/signup")
def signup(user: UserSignup):
    return s.signup(
        user.name,
        user.email,
        user.password,
        user.role
    )


@router.post("/login")
def login(user: UserLogin, response: Response):

    result = s.login(
        user.email,
        user.password
    )

    set_auth_cookies(
        response,
        result["access_token"],
        result["refresh_token"]
    )

    return {
        "message": "Login Successful"
    }


@router.post("/refresh")
def refresh(request: Request, response: Response):

    refresh_token = request.cookies.get("refresh_token")

    access_token = s.refresh_token(refresh_token)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="Lax",
        secure=False
    )

    return {
        "message": "Access Token Refreshed"
    }


@router.post("/logout")
def logout(
    response: Response,
    current_user=Depends(get_current_user)
):

    clear_auth_cookies(response)

    return {
        "message": "Logged Out Successfully"
    }