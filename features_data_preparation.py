import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

# fill in your details from spotify here
client_id = ''
client_secret = ''
username = ''

redirect_uri = 'https://localhost:3000'

# Create a Spotify client object with client credentials
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

data = pd.read_json('./mukul/StreamingHistory0.json')

# Getting Audio features
features_all = []

for track_name in data['trackName']:
    results = sp.search(q=track_name, type='track')
    track_id = results['tracks']['items'][0]['id']
    features = sp.audio_features(track_id)
    features_all.append(features[0])
    
data_dt = pd.DataFrame(features_all)
data_dt = pd.DataFrame(features_all)
data_dt['artistName'] = data['artistName']

# Getting Explicit and Popularity features
explicit = []
popularity = []
for id in data_dt.id:
    track = sp.track(id)
    explicit.append(track['explicit'])
    popularity.append(track['popularity'])
    
data_dt['explicit'] = explicit
data_dt['popularity'] = popularity

data_dt = data_dt.drop(columns=['Unnamed: 0', 'uri', 'track_href', 'analysis_url', 'type'])

data_dt.to_csv('mukul_info.csv')
