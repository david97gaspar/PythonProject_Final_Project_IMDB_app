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

def get_distinct_genres():

    conn = get_db_connection(); set_search_path(conn)
    cur  = conn.cursor()

    cur.execute("SELECT DISTINCT genre FROM movies WHERE genre IS NOT NULL;")
    genres = sorted(r[0] for r in cur.fetchall())
    cur.close(); conn.close()
    return genres

def get_movies_by_genre(genre: str):

    conn = get_db_connection(); set_search_path(conn)
    cur  = conn.cursor()
    if genre == "All":
        cur.execute("""
            SELECT id, title, release_year, imdb_rating, director, actors
              FROM movies
             ORDER BY imdb_rating DESC NULLS LAST;
        """)
    else:
        cur.execute("""
            SELECT id, title, release_year, imdb_rating, director, actors
              FROM movies
             WHERE LOWER(genre) = LOWER(%s)
             ORDER BY imdb_rating DESC NULLS LAST;
        """, (genre,))
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

