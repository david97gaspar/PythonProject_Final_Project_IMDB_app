
from database import get_db_connection, set_search_path


def get_all_movies():

    conn = get_db_connection()
    set_search_path(conn, "final_project")
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies;")
    movies = cur.fetchall()
    cur.close()
    conn.close()
    return movies


if __name__ == "__main__":
    movies = get_all_movies()
    for movie in movies:
        print(movie)
