
import gradio as gr
from movies import get_all_movies
from auth import register_user, login_user
from database import get_db_connection, set_search_path


from database import get_db_connection as _get_conn
def insert_rating(user_id, movie_id, rating):
    conn = _get_conn()
    set_search_path(conn)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO ratings (user_id, movie_id, score) VALUES (%s, %s, %s);",
        (user_id, movie_id, rating)
    )
    conn.commit()
    cur.close()
    conn.close()

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
    return [
        {"id": r[0], "title": r[1], "year": r[2],
         "genre": r[3], "director": r[4], "actors": r[5]}
        for r in rows
    ]

def sign_up(username, password):
    return register_user(username, password)

def sign_in(username, password):
    user_id = login_user(username, password)
    if user_id:
        return f"Welcome, user {user_id}!", user_id
    else:
        return "Invalid credentials.", None

def rate_movie(movie_id, rating, user_id):
    if user_id is None:
        return "You must sign in first!"
    insert_rating(user_id, movie_id, rating)
    return f" Rated movie {movie_id} with {rating} (user {user_id})."

def add_to_watchlist_ui(movie_id, user_id):
    if user_id is None:
        return " You must sign in first!"
    insert_watchlist(user_id, movie_id)
    return f" Added movie {movie_id} to watchlist (user {user_id})."

with gr.Blocks() as demo:
    gr.Markdown("## 🎬 Film Recommendation App with Auth")

    user_state = gr.State(value=None)

    with gr.Tab("Movies"):
        df = gr.DataFrame(
            headers=["ID","Title","Year","Genre","Director","Actors"],
            interactive=False, label="Our Catalogue"
        )
        gr.Button("Refresh").click(display_movies, [], df)

    with gr.Tab("Sign Up"):
        su_user = gr.Textbox(label="Username")
        su_pass = gr.Textbox(label="Password", type="password")
        su_btn = gr.Button("Create Account")
        su_out = gr.Textbox(label="Status")
        su_btn.click(sign_up, [su_user, su_pass], su_out)

    with gr.Tab("Sign In"):
        si_user = gr.Textbox(label="Username")
        si_pass = gr.Textbox(label="Password", type="password")
        si_btn = gr.Button("Log In")
        si_out = gr.Textbox(label="Status")
        # sign_in returns (message, user_id)
        si_btn.click(sign_in, [si_user, si_pass], [si_out, user_state])

    with gr.Tab("Rate Movie"):
        rm_id = gr.Number(label="Movie ID")
        rm_score = gr.Slider(1, 10, label="Rating")
        rm_btn = gr.Button("Submit Rating")
        rm_out = gr.Textbox(label="Status")
        rm_btn.click(rate_movie, [rm_id, rm_score, user_state], rm_out)

    with gr.Tab("Watchlist"):
        wl_id = gr.Number(label="Movie ID")
        wl_btn = gr.Button("Add to Watchlist")
        wl_out = gr.Textbox(label="Status")
        wl_btn.click(add_to_watchlist_ui, [wl_id, user_state], wl_out)

if __name__ == "__main__":
    demo.launch()
