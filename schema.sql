CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    title TEXT,
    place TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);