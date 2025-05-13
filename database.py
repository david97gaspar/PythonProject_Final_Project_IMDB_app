import psycopg2, json
import os

with open("config.json","r") as f:
    cfg = json.load(f)

DATABASE_URL = os.environ.get("DATABASE_URL", cfg["DATABASE_URL"])

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def set_search_path(conn, schema="final_project"):
    cur = conn.cursor()
    cur.execute("SET search_path TO %s;", (schema,))
    conn.commit()
    cur.close()


