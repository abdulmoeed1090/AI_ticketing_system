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


-- ==========================
-- CHAT HISTORY
-- ==========================

CREATE TABLE chat_history (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INTEGER NOT NULL,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id) REFERENCES users(id)
    
    
    
   -- ==========================
-- DUMMY USERS
-- ==========================

INSERT INTO users (name, email, password, role)
VALUES
('Admin', 'admin@gmail.com', 'admin123', 'admin'),
('Ali Khan', 'agent@gmail.com', 'agent123', 'agent'),
('Ahmed Raza', 'customer@gmail.com', 'customer123', 'customer');


-- ==========================
-- DUMMY TICKETS
-- ==========================

INSERT INTO tickets (title, description, status, customer_id, agent_id)
VALUES
(
'Cannot Login',
'I am unable to login after changing my password.',
'Open',
3,
2
),
(
'Assignment Upload Error',
'I receive an error while uploading my assignment PDF.',
'In Progress',
3,
2
),
(
'Forgot Password',
'I forgot my account password and cannot reset it.',
'Closed',
3,
2
);


-- ==========================
-- DUMMY CHAT HISTORY
-- ==========================

INSERT INTO chat_history (user_id, user_message, ai_response)
VALUES
(
3,
'I cannot login to my account.',
'Please make sure your email and password are correct. If the issue continues, use the Forgot Password option.'
),
(
3,
'How can I upload my assignment?',
'Go to the Assignments section, choose your course, and click Upload Assignment.'
),
(
2,
'Generate a professional reply for this customer.',
'Thank you for contacting support. We are currently investigating your issue and will update you shortly.'
);



