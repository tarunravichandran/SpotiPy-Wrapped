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
    cache_path=".spotipyoauthcache"  # Cache token
)

st.title("Show 5 Long-Term Top Tracks")

# Check if the user is already logged in (token cached)
token_info = auth_manager.get_cached_token()

if token_info:
    # Already have a token, user is logged in
    sp = spotipy.Spotify(auth_manager=auth_manager)
    # Fetch 5 long-term top tracks
    top_tracks_long = sp.current_user_top_tracks(limit=5, time_range="long_term")
    st.write("Your top 5 long-term tracks:")
    for idx, track in enumerate(top_tracks_long['items'], start=1):
        st.write(f"{idx}. {track['name']} by {track['artists'][0]['name']}")
else:
    # Not logged in yet, handle the OAuth flow
    query_params = st.experimental_get_query_params()
    if "code" in query_params:
        # There's a code in the URL; exchange it for a token
        code = query_params["code"][0]
        auth_manager.get_access_token(code)  # This stores the token in the cache
        st.experimental_rerun()
    else:
        # No code, no token: show login link
        auth_url = auth_manager.get_authorize_url()
        st.write(f"[Login with Spotify]({auth_url})")
