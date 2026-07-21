from fastapi import HTTPException

from src.connection.conn import get_connection


def get_all_tickets():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            t.id,
            t.title,
            t.description,
            t.status,
            customer.name,
            agent.name,
            t.created_at
        FROM tickets t
        JOIN users customer
            ON t.customer_id = customer.id
        LEFT JOIN users agent
            ON t.agent_id = agent.id
        ORDER BY t.id;
    """)

    tickets = cursor.fetchall()

    cursor.close()
    conn.close()

    return tickets


def get_ticket(ticket_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM tickets
        WHERE id=%s;
        """,
        (ticket_id,)
    )

    ticket = cursor.fetchone()

    cursor.close()
    conn.close()

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found."
        )

    return ticket


def create_ticket(title: str, description: str, customer_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tickets
        (
            title,
            description,
            customer_id
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
            title,
            description,
            customer_id
        )
    )

    ticket_id = cursor.fetchone()[0]

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Ticket created successfully.",
        "ticket_id": ticket_id
    }


def update_ticket(ticket_id, title, description, status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM tickets
        WHERE id=%s;
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

    cursor.execute(
        """
        UPDATE tickets
        SET
            title=%s,
            description=%s,
            status=%s
        WHERE id=%s;
        """,
        (
            title,
            description,
            status,
            ticket_id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Ticket updated successfully."
    }


def delete_ticket(ticket_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM tickets
        WHERE id=%s;
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

    cursor.execute(
        """
        DELETE FROM tickets
        WHERE id=%s;
        """,
        (ticket_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Ticket deleted successfully."
    }