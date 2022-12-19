import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
import pprint
client_id = "0b58d249bcd04325a7bbc9e146de3926"
client_secret = "a43661f1e20040ddb2017c6e23559afe"
redirect = "http://example.com"

date = input("Which date you wish to time travel to? Mention in YYYY-MM-DD format please.")
biilboard_url = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(biilboard_url)
html_data = response.text
soup = BeautifulSoup(html_data, "html.parser")
song_titles = soup.select(".o-chart-results-list__item #title-of-a-story")
list_songs = [song.string.strip() for song in song_titles]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
song_uris = []

for song in list_songs:
    search_uri = sp.search(q=f"track:{song} year{date.split('-')[0]}", type="track")
    try:
        uri = search_uri["tracks"]["items"][0]["uri"]
        song_uris.append(uri)

    except:
        print(f"{song} not found.Skipped")
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
playlist_id = playlist["id"]

sp.playlist_replace_items(playlist_id=playlist_id, items=song_uris)