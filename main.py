from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "playlist-modify-private"

SPOTIFY_CLIENT_ID = "e50ecb793bd341eb823e5170b0d35138"
SPOTIFY_SECRET = "bf34a7c9f3b446a6ba73e1a2c905c5df"

date = input("What date would you like to travel to?: eg. YYYY-MM-DD: ")

SONGS_URL = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(SONGS_URL)
website = response.text

soup = BeautifulSoup(website, "html.parser")

songs = soup.select(selector="li ul li h3")
song_names = [song.getText().strip("\n") for song in songs]
# print(song_names)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
