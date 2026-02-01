import db

def add_event(title, place, user_id):
    sql = "INSERT INTO events (title, place, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [title, place, user_id])
    event_id = db.last_insert_id()
    return event_id

def get_event(event_id):
    sql = "SELECT id, title, place FROM events WHERE id = ?"
    return db.query(sql, [event_id])[0]