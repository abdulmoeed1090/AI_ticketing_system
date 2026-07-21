from fastapi import HTTPException

from src.connection.conn import get_connection
from src.security.hashing import hash_password, verify_password
from src.security.jwt_handler import (
    create_access_token,
    create_refresh_token,
    decode_token
)


def signup(name: str, email: str, password: str, role: str):

    conn = get_connection()
    cursor = conn.cursor()

    # Check if email already exists
    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE email = %s;
        """,
        (email,)
    )

    if cursor.fetchone():

        cursor.close()
        conn.close()

        raise HTTPException(
            status_code=400,
            detail="Email already exists."
        )

    hashed_password = hash_password(password)

    cursor.execute(
        """
        INSERT INTO users(name, email, password, role)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """,
        (name, email, hashed_password, role)
    )

    user_id = cursor.fetchone()[0]

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "User registered successfully.",
        "user_id": user_id
    }


def login(email: str, password: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, email, password, role
        FROM users
        WHERE email = %s;
        """,
        (email,)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    if not verify_password(password, user[3]):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    payload = {
        "id": user[0],
        "name": user[1],
        "email": user[2],
        "role": user[4]
    }

    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)

    return {
        "message": "Login successful.",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "role": user[4]
        }
    }


def refresh_token(refresh_token: str):

    if refresh_token is None:
        raise HTTPException(
            status_code=401,
            detail="Refresh token is missing."
        )

    try:
        payload = decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token."
            )

        new_payload = {
            "id": payload["id"],
            "name": payload["name"],
            "email": payload["email"],
            "role": payload["role"]
        }

        new_access_token = create_access_token(new_payload)

        return new_access_token

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token."
        )


def logout():

    return {
        "message": "Logged out successfully."
    }