CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    title TEXT,
    location TEXT,
    description TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    user_id INTEGER REFERENCES users
);

CREATE TABLE rsvps (
    id INTEGER PRIMARY KEY,
    status INTEGER,
    diet TEXT,
    snack TEXT,
    greetings TEXT,
    user_id INTEGER REFERENCES users,
    event_id INTEGER REFERENCES events
);

CREATE TABLE types (
    id INTEGER PRIMARY KEY,
    title TEXT
);

CREATE TABLE event_types (
    id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES events
);