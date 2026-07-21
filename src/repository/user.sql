-- ==========================
-- USERS
-- ==========================

CREATE TABLE users (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin', 'agent', 'customer')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
