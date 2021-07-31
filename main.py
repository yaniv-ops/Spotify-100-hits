import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

URL = "https://www.billboard.com/charts/hot-100"
date = input('What year would you like to go back to(YYYY-MM-DD)?')
response = requests.get(f"{URL}/{date}")
billboard_html = response.text
client_id = 'ec47f463ec2b42eb862033a3f527a82c'
spotify_secret = '76ecd105a1674a5aaad6390e6b0eac4f'

soup = BeautifulSoup(billboard_html, 'html.parser')



number = soup.find_all(name='span', class_='chart-element__information__song text--truncate color--primary')

songs_list = [song.getText() for song in number]
print(songs_list)
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(scope="playlist-modify-private",
        redirect_uri="http://127.0.0.1:5500/",
        client_id=client_id,
        client_secret=spotify_secret,
        show_dialog=True,
        cache_path="token.txt",
                              )
)

user_id = sp.current_user()['id']
print(user_id)
year = date.split('-')[0]
print(year)
list_of_uri = []
for song in songs_list:
    result = sp.search(q=f"track:{song} year:{year}", type='track')
    try:
        list_of_uri.append(result['tracks']['items'][0]['uri'])
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
print(list_of_uri)

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=list_of_uri)