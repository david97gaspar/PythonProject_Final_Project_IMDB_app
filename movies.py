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


def get_movie_id_by_title(title: str):

    conn = get_db_connection()
    set_search_path(conn)
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM movies WHERE LOWER(title) = LOWER(%s);",
        (title.strip(),)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row else None
