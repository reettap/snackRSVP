import db

def add_event(title, place, user_id):
    sql = "INSERT INTO events (title, place, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [title, place, user_id])
    event_id = db.last_insert_id()
    return event_id

def get_event(event_id):
    sql = "SELECT id, title, place, user_id FROM events WHERE id = ?"
    result = db.query(sql, [event_id])
    return result[0] if result else None

def get_events():
    sql = "SELECT id, title, place, user_id FROM events"
    result = db.query(sql)
    return result

def search(query):
    sql = """SELECT id, title, place, user_id
             FROM events
             WHERE title LIKE ?"""
    result = db.query(sql, ["%" + query + "%"])
    return result

def delete_event(event_id):
    sql = "DELETE FROM events WHERE id = ?"
    db.execute(sql, [event_id])

def update_event(event_id, title, place):
    sql = "UPDATE events SET title = ?, place = ? WHERE id = ?"
    db.execute(sql, [title, place, event_id])
