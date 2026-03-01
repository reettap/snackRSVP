import db

def add_event(title, location, description,
              start_time, end_time, user_id):
    sql = """INSERT INTO 
                events (title, location, description, 
                        start_time, end_time, user_id) 
            VALUES (?, ?, ?, ?, ?, ?)
          """
    db.execute(sql, [title, location, description, start_time, end_time, user_id])
    event_id = db.last_insert_id()
    return event_id

def get_event(event_id):
    sql = """SELECT id, title, location, description, 
                    start_time, end_time, user_id 
             FROM events 
             WHERE id = ?"""
    result = db.query(sql, [event_id])
    return result[0] if result else None

def get_events():
    sql = """SELECT id, title, location, description, start_time, end_time, user_id FROM events"""
    result = db.query(sql)
    return result

def get_events_by_organizer(user_id):
    sql = """SELECT id, title, location, description, start_time, end_time, user_id FROM events WHERE user_id = ?"""
    result = db.query(sql, [user_id])
    return result

def search(query):
    sql = """SELECT id, title, location, description, start_time, end_time, user_id
             FROM events
             WHERE title LIKE ?"""
    result = db.query(sql, ["%" + query + "%"])
    return result

def delete_event(event_id):
    sql = "DELETE FROM rsvps WHERE event_id = ?"
    db.execute(sql, [event_id])
    sql = "DELETE FROM events WHERE id = ?"
    db.execute(sql, [event_id])

def update_event(event_id, title, location, description, start_time, end_time):
    sql = """UPDATE events SET 
                title = ?, 
                location = ?,
                description = ?,
                start_time = ?,
                end_time = ?
            WHERE id = ?"""
    db.execute(sql, [title, location, description, start_time, end_time, event_id])

def add_rsvp(status, diet, snack, greetings, event_id, user_id):
    sql = """INSERT INTO rsvps (status, diet, snack, greetings, event_id, user_id) 
             VALUES (?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [status, diet, snack, greetings, event_id, user_id])

def get_rsvp(event_id, user_id):
    sql = """SELECT status, diet, snack, greetings, event_id, user_id 
             FROM rsvps WHERE event_id = ? AND user_id = ?"""
    result = db.query(sql, [event_id, user_id])
    return result[0] if result else None

def get_rsvps_by_event(event_id):
    sql = """SELECT 
                r.status, 
                r.diet, 
                r.snack, 
                r.greetings, 
                r.event_id, 
                r.user_id,
                u.username 
             FROM rsvps as r JOIN users as u  ON u.id = r.user_id
             WHERE r.event_id = ?"""
    result = db.query(sql, [event_id])
    return result

def get_snacks_by_event(event_id):
    sql = """SELECT snack
             FROM rsvps
             WHERE event_id = ?"""
    result = db.query(sql, [event_id])
    return result

def get_diets_by_event(event_id):
    sql = """SELECT diet
             FROM rsvps
             WHERE event_id = ?"""
    result = db.query(sql, [event_id])
    return result

def get_attendees_by_event(event_id):
    sql = """SELECT DISTINCT u.username
             FROM rsvps as r JOIN users as u  ON u.id = r.user_id
             WHERE r.event_id = ?"""
    result = db.query(sql, [event_id])
    return result

def get_attending_events_for_user(user_id):
    sql = """SELECT
                 DISTINCT r.event_id,
                 e.id, e.title, e.location, e.description, 
                 e.start_time, e.end_time, e.user_id
             FROM rsvps as r JOIN events as e  ON e.id = r.event_id
             WHERE r.user_id = ?"""
    result = db.query(sql, [user_id])
    return result