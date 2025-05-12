# 🎬 The Movie Base

A lightweight film-recommendation web app built with Gradio and PostgreSQL.  
Users can sign up, sign in, rate films, manage a personal watchlist, and view their own ratings.

---

## Features

- 📋 Browse a pre-populated catalogue of films (title, year, director, actors, IMDb rating)  
- 🔒 User authentication (sign up / sign in / sign out)  
- ⭐ Rate films (first-time rate + update via “Change Rating”)  
- 👍 Add or remove films from your watchlist  
- 📑 “My Watchlist” and “My Ratings” dashboards  
- ⚙️ Configurable via `config.json`  
- 🔧 Easily containerized with Docker

---

## Project Structure

film-app/
├── app.py # Gradio UI
├── callbacks.py # Gradio callbacks
├── movies.py # Core movie queries
├── user_data.py # Watchlist & ratings queries
├── auth.py # User sign-up / sign-in
├── database.py # DB connection & schema helper
├── fetch_ratings_omdb.py # Fill imdb_rating via OMDb
├── styles.css # Custom CSS
├── config.json # DB URL & OMDb key
├── requirements.txt # Python dependencies
├── README.md # This file
└── Dockerfile # Container build