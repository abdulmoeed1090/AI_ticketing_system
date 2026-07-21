from fastapi import HTTPException

from src.connection.conn import get_connection


def get_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name,
            email,
            role,
            created_at
        FROM users
        ORDER BY id;
        """
    )

    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return users


def get_user(user_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name,
            email,
            role,
            created_at
        FROM users
        WHERE id = %s;
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    return user


def delete_user(user_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE id = %s;
        """,
        (user_id,)
    )

    if cursor.fetchone() is None:

        cursor.close()
        conn.close()

        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    cursor.execute(
        """
        DELETE FROM users
        WHERE id = %s;
        """,
        (user_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "User deleted successfully."
    }


def assign_ticket(ticket_id: int, agent_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    # Check ticket exists
    cursor.execute(
        """
        SELECT id
        FROM tickets
        WHERE id = %s;
        """,
        (ticket_id,)
    )

    if cursor.fetchone() is None:

        cursor.close()
        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Ticket not found."
        )

    # Check agent exists
    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE id = %s
        AND role = 'agent';
        """,
        (agent_id,)
    )

    if cursor.fetchone() is None:

        cursor.close()
        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Agent not found."
        )

    cursor.execute(
        """
        UPDATE tickets
        SET
            agent_id = %s,
            status = 'In Progress'
        WHERE id = %s;
        """,
        (agent_id, ticket_id)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Ticket assigned successfully."
    }


def get_all_tickets():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            t.id,
            t.title,
            t.description,
            t.status,
            customer.name AS customer,
            agent.name AS agent,
            t.created_at
        FROM tickets t
        JOIN users customer
            ON customer.id = t.customer_id
        LEFT JOIN users agent
            ON agent.id = t.agent_id
        ORDER BY t.id;
        """
    )

    tickets = cursor.fetchall()

    cursor.close()
    conn.close()

    return tickets