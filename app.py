import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

st.title("My Spotify Top Tracks")

# Load secrets from st.secrets
client_id = st.secrets["SPOTIPY_CLIENT_ID"]
client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
redirect_uri = st.secrets["SPOTIPY_REDIRECT_URI"]

scope = "user-top-read"

# Initialize SpotifyOAuth object
auth_manager = SpotifyOAuth(client_id=client_id,
                            client_secret=client_secret,
                            redirect_uri=redirect_uri,
                            scope=scope,
                            show_dialog=True,
                            cache_path=".spotipyoauthcache")

# Check if user has been authenticated (access token cached)
if auth_manager.get_cached_token():
    # User already authenticated
    sp = spotipy.Spotify(auth_manager=auth_manager)
    st.write("You are logged in!")
    
    # Fetch top tracks
    top_tracks = sp.current_user_top_tracks(limit=10, time_range="short_term")
    track_names = [item['name'] for item in top_tracks['items']]
    st.write("Your top 10 tracks (short term):")
    for idx, track in enumerate(track_names, start=1):
        st.write(f"{idx}. {track}")
else:
    # Not logged in yet
    auth_url = auth_manager.get_authorize_url()
    st.write("Please [login with Spotify]("+auth_url+")")

    # Instructions for user:
    # Once they click the link, they'll go to Spotify's login page, 
    # then get redirected back to redirect_uri. For local testing, you may have to copy-paste the code parameter back into app or just re-run after caching is done.

    # If you want a smoother experience, you might implement a query parameter check:
    # if "code" in st.experimental_get_query_params():
    #     code = st.experimental_get_query_params()["code"]
    #     token_info = auth_manager.get_access_token(code)
    #     st.experimental_rerun()
