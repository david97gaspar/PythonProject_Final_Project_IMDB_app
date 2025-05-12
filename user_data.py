from database import get_db_connection, set_search_path


def get_user_watchlist(user_id: int):

    conn = get_db_connection()
    set_search_path(conn)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT m.id, m.title, m.release_year, m.genre,
               m.director, m.actors, m.imdb_rating
          FROM watchlist w
          JOIN movies   m ON w.movie_id = m.id
         WHERE w.user_id = %s;
        """,
        (user_id,)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_user_ratings(user_id: int):

    conn = get_db_connection()
    set_search_path(conn)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT m.id, m.title, m.release_year, m.genre,
               m.director, m.actors, m.imdb_rating,
               r.rating
          FROM ratings r
          JOIN movies  m ON r.movie_id = m.id
         WHERE r.user_id = %s;
        """,
        (user_id,)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
