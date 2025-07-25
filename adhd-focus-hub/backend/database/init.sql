CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    hashed_password VARCHAR(256) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    owner_id INTEGER REFERENCES users(id),
    title VARCHAR(200),
    description VARCHAR(1000),
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE mood_logs (
    id SERIAL PRIMARY KEY,
    owner_id INTEGER REFERENCES users(id),
    mood_score INTEGER,
    notes VARCHAR(1000),
    created_at TIMESTAMP NOT NULL
);

