
-- ==========================
-- TICKETS
-- ==========================

CREATE TABLE tickets (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    title TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT DEFAULT 'Open'
        CHECK(status IN ('Open', 'In Progress', 'Closed')),
    customer_id INTEGER NOT NULL,
    agent_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(customer_id) REFERENCES users(id),
    FOREIGN KEY(agent_id) REFERENCES users(id)
);

