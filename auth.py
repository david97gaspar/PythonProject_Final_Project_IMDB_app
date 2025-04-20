import psycopg2, json, bcrypt
from database import get_db_connection, set_search_path


with open("config.json", "r") as f:
    config = json.load(f)

def create_user_table():

    conn = get_db_connection()
    set_search_path(conn)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
      id SERIAL PRIMARY KEY,
      username VARCHAR(255) UNIQUE NOT NULL,
      password_hash VARCHAR(255) NOT NULL
    );
    """)
    conn.commit()
    cur.close()
    conn.close()

def register_user(username, password):

    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    conn = get_db_connection()
    set_search_path(conn)
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s);",
            (username, pw_hash)
        )
        conn.commit()
        message = "User created!"
    except psycopg2.IntegrityError:
        conn.rollback()
        message = "Username already exists."
    cur.close()
    conn.close()
    return message

def login_user(username, password):

    conn = get_db_connection()
    set_search_path(conn)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, password_hash FROM users WHERE username = %s;",
        (username,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return None
    user_id, pw_hash = row
    return user_id if bcrypt.checkpw(password.encode(), pw_hash.encode()) else None

if __name__ == "__main__":
    create_user_table()
    print(register_user("david", "12345"))
    print(register_user("david", "again"))
    uid = login_user("david", "12345")
    print("Logged in, user id =", uid)
