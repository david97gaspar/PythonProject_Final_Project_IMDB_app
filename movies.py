from database import get_db_connection, set_search_path

def get_all_movies():
    conn = get_db_connection()
    set_search_path(conn)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, title, release_year, imdb_rating, director, actors
          FROM movies;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
