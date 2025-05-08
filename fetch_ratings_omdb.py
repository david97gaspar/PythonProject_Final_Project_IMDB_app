
import json, time, requests
from database import get_db_connection, set_search_path


with open("config.json", "r") as f:
    cfg = json.load(f)
OMDB_KEY = cfg["OMDB_API_KEY"]

def fetch_and_store():
    conn = get_db_connection()
    set_search_path(conn, "final_project")
    cur = conn.cursor()


    cur.execute("SELECT id, title, release_year FROM movies;")
    movies = cur.fetchall()

    for mid, title, year in movies:
        params = {"t": title, "y": year, "apikey": OMDB_KEY}
        resp = requests.get("http://www.omdbapi.com/", params=params).json()
        raw = resp.get("imdbRating", "N/A")
        try:
            rating = float(raw) if raw != "N/A" else None
        except ValueError:
            rating = None

        cur.execute(
            "UPDATE movies SET imdb_rating = %s WHERE id = %s;",
            (rating, mid)
        )
        print(f"{mid}: {title} ({year}) → {rating}")
        time.sleep(0.1)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ All ratings updated.")

if __name__ == "__main__":
    fetch_and_store()
