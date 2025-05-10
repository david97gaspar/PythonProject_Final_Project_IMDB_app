import gradio as gr
import callbacks as cb

with open("styles.css", "r") as css_file:
    custom_css = css_file.read()

with gr.Blocks(theme=gr.themes.Soft(), css=custom_css) as demo:

    gr.Markdown("## 🎬 **The Movie Base**", elem_id="header-markdown")

    user_state = gr.State(value=None)


    with gr.Tab("Movies"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Filter by Genre")
                genre_dd = gr.Dropdown(
                    choices=cb.list_genres(),
                    value="All",
                    interactive=True
                )
            with gr.Column(scale=3):
                movies_df = gr.DataFrame(
                    headers=["ID","Title","Year","IMDb Rating","Director","Actors"],
                    interactive=False,
                    label="Catalogue"
                )
        genre_dd.change(
            fn=cb.display_by_genre,
            inputs=[genre_dd],
            outputs=[movies_df],
        )

        cb.display_by_genre("All")


    with gr.Tab("Sign Up"):
        gr.Markdown("### Create a New Account")
        su_user = gr.Textbox(label="Username")
        su_pass = gr.Textbox(label="Password", type="password")
        su_btn  = gr.Button("Create Account")
        su_out  = gr.Textbox(label="Status")
        su_btn.click(cb.sign_up, [su_user, su_pass], su_out)


    with gr.Tab("Sign In"):
        gr.Markdown("### Log In / Out")
        si_user = gr.Textbox(label="Username")
        si_pass = gr.Textbox(label="Password", type="password")
        si_btn  = gr.Button("Log In")
        si_out  = gr.Textbox(label="Status")
        si_btn.click(cb.sign_in, [si_user, si_pass], [si_out, user_state])

        so_btn  = gr.Button("Log Out", elem_id="logout-btn")
        so_out  = gr.Textbox(label="Status")
        so_btn.click(cb.sign_out, [user_state], [so_out, user_state])


    with gr.Tab("Rate Movie"):
        gr.Markdown("### Rate a Movie")
        title_in = gr.Textbox(label="Movie Title")
        score_in = gr.Slider(label="Your Rating", minimum=1, maximum=10, step=1)
        rm_btn   = gr.Button("Submit Rating")
        rm_out   = gr.Textbox(label="Status")
        rm_btn.click(cb.rate_movie_by_title, [title_in, score_in, user_state], rm_out)


    with gr.Tab("Watchlist"):
        gr.Markdown("### Add to Your Watchlist")
        title_wl = gr.Textbox(label="Movie Title")
        wl_btn   = gr.Button("Add to Watchlist")
        wl_out   = gr.Textbox(label="Status")
        wl_btn.click(cb.add_to_watchlist_by_title, [title_wl, user_state], wl_out)


    with gr.Tab("My Watchlist"):
        wl_df   = gr.DataFrame(
            headers=["ID","Title","Year","Genre","Director","Actors","IMDb Rating"],
            interactive=False
        )
        refresh = gr.Button("Refresh My Watchlist")
        refresh.click(cb.display_watchlist, [user_state], wl_df)

        gr.Markdown("### Remove from Watchlist")
        rem_title = gr.Textbox(label="Title to Remove")
        rem_btn   = gr.Button("Remove from Watchlist")
        rem_out   = gr.Textbox(label="Status")
        rem_btn.click(cb.remove_from_watchlist_by_title, [rem_title, user_state], rem_out)


    with gr.Tab("My Ratings"):
        rt_df    = gr.DataFrame(
            headers=["ID","Title","Year","Genre","Director","Actors","IMDb Rating","My Rating"],
            interactive=False
        )
        refresh2 = gr.Button("Refresh My Ratings")
        refresh2.click(cb.display_my_ratings, [user_state], rt_df)


    with gr.Tab("Change Rating"):
        gr.Markdown("### Update an Existing Rating")
        title_cr = gr.Textbox(label="Movie Title")
        score_cr = gr.Slider(label="New Rating", minimum=1, maximum=10, step=1)
        upd_btn  = gr.Button("Update Rating")
        upd_out  = gr.Textbox(label="Status")
        upd_btn.click(cb.change_rating_by_title, [title_cr, score_cr, user_state], upd_out)

if __name__ == "__main__":
    demo.launch()