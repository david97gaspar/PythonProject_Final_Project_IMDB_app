import bcrypt, json, psycopg2
from database import get_db_connection, set_search_path

with open("config.json","r") as f:
    cfg = json.load(f)


def register_user(username, password):

    if len(password) < 5:
        return "⚠️ Password must be at least 5 characters long."


    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    conn = get_db_connection()
    set_search_path(conn)
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO users (username, password_hash) 
            VALUES (%s, %s);
        """, (username, pw_hash))
        conn.commit()
        msg = "✅ User created!"
    except psycopg2.IntegrityError:
        conn.rollback()
        msg = "⚠️ Username already exists."
    finally:
        cur.close()
        conn.close()

    return msg


def login_user(username, password):
    conn = get_db_connection(); set_search_path(conn)
    cur = conn.cursor()
    cur.execute("SELECT id,password_hash FROM users WHERE username=%s;", (username,))
    row = cur.fetchone(); cur.close(); conn.close()
    if not row: return None
    uid, pw_hash = row
    return uid if bcrypt.checkpw(password.encode(), pw_hash.encode()) else None


