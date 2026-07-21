from fastapi import HTTPException

from src.connection.conn import get_connection


def chat(user_id: int, message: str):

    # AI Integration will be added later.
    ai_response = "AI integration coming soon."

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chat_history
        (
            user_id,
            user_message,
            ai_response
        )
        VALUES
        (
            %s,
            %s,
            %s
        )
        RETURNING id;
        """,
        (
            user_id,
            message,
            ai_response
        )
    )

    chat_id = cursor.fetchone()[0]

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "chat_id": chat_id,
        "user_message": message,
        "ai_response": ai_response
    }


def get_chat_history(user_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            user_message,
            ai_response,
            created_at
        FROM chat_history
        WHERE user_id=%s
        ORDER BY created_at DESC;
        """,
        (user_id,)
    )

    chats = cursor.fetchall()

    cursor.close()
    conn.close()

    return chats


def delete_chat(chat_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM chat_history
        WHERE id=%s;
        """,
        (chat_id,)
    )

    if cursor.fetchone() is None:

        cursor.close()
        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Chat not found."
        )

    cursor.execute(
        """
        DELETE FROM chat_history
        WHERE id=%s;
        """,
        (chat_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Chat deleted successfully."
    }