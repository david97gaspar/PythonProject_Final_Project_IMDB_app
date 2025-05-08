import gradio as gr
import callbacks as cb


with gr.Blocks() as demo:
    gr.Markdown("## 🎬 The Movie Base")

    user_state = gr.State(value=None)

    with gr.Tab("Movies"):
        df = gr.DataFrame(
            headers=["ID","Title","Year","IMDb Rating","Director","Actors"],
            interactive=False
        )
        gr.Button("Refresh").click(cb.display_movies, [], df)

    with gr.Tab("Sign Up"):
        u,p = gr.Textbox("Username"), gr.Textbox("Password", type="password")
        o    = gr.Textbox("Status")
        gr.Button("Create Account").click(cb.sign_up, [u,p], o)

    with gr.Tab("Sign In"):
        u2,p2 = gr.Textbox("Username"), gr.Textbox("Password", type="password")
        o2    = gr.Textbox("Status")
        gr.Button("Log In").click(cb.sign_in, [u2,p2], [o2,user_state])

    with gr.Tab("Rate Movie"):
        title_in = gr.Textbox("Movie Title")
        score_in = gr.Slider(1,10, step = 1)
        out1     = gr.Textbox("Status")
        gr.Button("Submit Rating").click(
            cb.rate_movie_by_title, [title_in,score_in,user_state], out1
        )

    with gr.Tab("Watchlist"):
        title_wl = gr.Textbox("Movie Title")
        out2     = gr.Textbox("Status")
        gr.Button("Add to Watchlist").click(
            cb.add_to_watchlist_by_title, [title_wl,user_state], out2
        )

    with gr.Tab("My Watchlist"):
        wl_df = gr.DataFrame(
            headers=["ID","Title","Year","Genre","Director","Actors","IMDb Rating"],
            interactive=False
        )
        gr.Button("Refresh My Watchlist").click(
            cb.display_watchlist, [user_state], wl_df
        )
        rem_title = gr.Textbox(label="Title to Remove")
        rem_btn = gr.Button("Remove from Watchlist")
        rem_out = gr.Textbox(label="Status")
        rem_btn.click(
            cb.remove_from_watchlist_by_title,
            inputs=[rem_title, user_state],
            outputs=rem_out
        )

    with gr.Tab("My Ratings"):
        rt_df = gr.DataFrame(
            headers=["ID","Title","Year","Genre","Director","Actors","IMDb Rating","My Rating"],
            interactive=False
        )
        gr.Button("Refresh My Ratings").click(
            cb.display_my_ratings, [user_state], rt_df
        )
    with gr.Tab("Change Rating"):
        title_up = gr.Textbox(label="Movie Title")
        score_up = gr.Slider(1, 10, step=1, label="New Rating")
        upd_btn = gr.Button("Update Rating")
        upd_out = gr.Textbox(label="Status")
        upd_btn.click(
            cb.rate_movie_by_title,
            inputs=[title_up, score_up, user_state],
            outputs=upd_out
        )

if __name__ == "__main__":
    demo.launch()
