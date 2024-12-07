import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set the scope to read user's top tracks
scope = "user-top-read"

# Initialize the auth manager using secrets
auth_manager = SpotifyOAuth(
    client_id=st.secrets["SPOTIPY_CLIENT_ID"],
    client_secret=st.secrets["SPOTIPY_CLIENT_SECRET"],
    redirect_uri=st.secrets["SPOTIPY_REDIRECT_URI"],
    scope=scope,
    show_dialog=True,
)

st.title("SpotiPY Wrapped - Top 5 Songs Since Day 1 of Spotify")

# Function to fetch and display tracks
def display_top_tracks():
    try:
        sp = spotipy.Spotify(auth_manager=auth_manager)
        top_tracks_long = sp.current_user_top_tracks(limit=5, time_range="long_term")
        st.write("Your top 5 long-term tracks:")
        for idx, track in enumerate(top_tracks_long['items'], start=1):
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            album_cover_url = track['album']['images'][0]['url']  # URL of the cover image
            st.image(album_cover_url, width=300)  # Display the cover image
            st.write(f"**{idx}. {track_name}** by **{artist_name}**")  # Song name and artist
    except Exception as e:
        st.error("There was an issue fetching your top tracks. Please refresh or try logging in again.")
        st.error(f"Error details: {e}")

# Check if the user is already logged in (token cached)
token_info = auth_manager.get_cached_token()

if token_info and not auth_manager.is_token_expired(token_info):
    # Valid token, display tracks
    display_top_tracks()
else:
    # Token is invalid or not available; handle the OAuth flow
    query_params = st.experimental_get_query_params()
    if "code" in query_params:
        try:
            code = query_params["code"][0]
            auth_manager.get_access_token(code)  # Exchange code for token and cache it
            st.experimental_rerun()  # Restart to use the new token
        except Exception as e:
            st.error("There was an issue with the login process. Please try again.")
            st.error(f"Error details: {e}")
    else:
        # No code in URL, show login link
        auth_url = auth_manager.get_authorize_url()
        st.write(f"[Login with Spotify]({auth_url})")
