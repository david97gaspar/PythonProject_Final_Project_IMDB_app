
from auth      import register_user, login_user
from movies    import get_all_movies, get_movie_id_by_title
from user_data import get_user_watchlist, get_user_ratings
from database  import get_db_connection as _get_conn, set_search_path

def insert_rating(user_id, movie_id, rating):


    conn = _get_conn()
    set_search_path(conn)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO ratings (user_id, movie_id, rating)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id, movie_id)
        DO UPDATE SET rating = EXCLUDED.rating;
        """,
        (user_id, movie_id, rating)
    )
    conn.commit()

    cur.close()
    conn.close()
    return f"✅ Your rating for movie {movie_id} has been set to {rating}."


def insert_watchlist(user_id, movie_id):
    conn = _get_conn()
    set_search_path(conn)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO watchlist (user_id, movie_id) VALUES (%s, %s);",
        (user_id, movie_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def display_movies():
    rows = get_all_movies()
    return [list(r) for r in rows]

def sign_up(u, p):
    return register_user(u, p)

def sign_in(u, p):
    uid = login_user(u, p)
    return (f"✅ Welcome, user {uid}!", uid) if uid else ("❌ Invalid credentials.", None)

def rate_movie_by_title(title, score, user_id):
    if user_id is None: return "❌ Sign in first!"
    mid = get_movie_id_by_title(title)
    if mid is None:   return f"❌ No movie titled “{title}.”"
    insert_rating(user_id, mid, score)
    return f"✅ Rated “{title}” with {score}."

def add_to_watchlist_by_title(title, user_id):
    if user_id is None: return "❌ Sign in first!"
    mid = get_movie_id_by_title(title)
    if mid is None:    return f"❌ No movie titled “{title}.”"
    insert_watchlist(user_id, mid)
    return f"✅ “{title}” added to watchlist."

def remove_from_watchlist_by_title(title, user_id):
    if user_id is None:
        return "❌ Sign in first!"
    mid = get_movie_id_by_title(title)
    if mid is None:
        return f"❌ No movie titled “{title}.”"
    conn = _get_conn(); set_search_path(conn)
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM watchlist WHERE user_id=%s AND movie_id=%s;",
        (user_id, mid)
    )
    conn.commit()
    deleted = cur.rowcount
    cur.close(); conn.close()
    return (
        f"✅ Removed “{title}” from your watchlist."
        if deleted
        else f"⚠️ “{title}” was not in your watchlist."
    )

def display_watchlist(user_id):
    rows = get_user_watchlist(user_id)
    return [list(r) for r in rows]

def display_my_ratings(user_id):
    rows = get_user_ratings(user_id)
    return [list(r) for r in rows]