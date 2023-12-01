#a lot of the code in this was borrowed from this youtube video https://www.youtube.com/watch?v=WAmEZBEeNmg&t=1248s
#importing dependancies
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import csv

#loading .env or environment file 
load_dotenv()

#loading in client id and client secret for Spotify web API
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

#getting authorization token with client id and client secret credentials
def get_token():
    #creating authorization string
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    #url to send auth request to and required arguments in headers
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

token = get_token()
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

#csv data necessary for spotify web api searches
csvpath = os.path.join('bootcamp-project-1','Resources','top_10k_streamed_songs.csv')

#songs, artists, and track ID's lists
song = []
artist = []
track_search = []

#reading in csv file for top 10k streamed songs 
with open(csvpath, 'r', encoding='utf-8') as csvfile:

    csvreader = csv.reader(csvfile, delimiter=',')
    
    csv_header = next(csvreader)
    
    #appending song names to song[] and artist names to artist[]
    for row in csvreader:
        song.append(row[2])
        artist.append(row[1])


#creating shortened lists to improve testing within the api
song_test = song[:20]
artist_test = artist[:20]


#searching for track id using track name and artists name, doing this because there are repeat song titles in the csv
def search_for_track(token, track_name, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={track_name} {artist_name}&type=track&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["tracks"]["items"]

    if len(json_result) == 0:
        print(f"No track with the name '{track_name}' by '{artist_name}' found.")
        return None
    else:
        return json_result[0]["id"]  # Return the track ID

# Iterate through all items in the song list and search for each track ID
for track_name, artist_name in zip(song_test, artist_test):
    # Search for track ID
    track_id = search_for_track(token, track_name, artist_name)

    if track_id:
        track_search.append(track_id)
        print(f"Track ID for '{track_name}' by '{artist_name}': {track_id}")
    else:
        print(f"Track ID not found for '{track_name}' by '{artist_name}'.")

#audio features segment
def get_audio_features(token, track_id):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    
    # Extract relevant audio features
    duration_ms = json_result["duration_ms"]
    energy = json_result["energy"]
    tempo = json_result["tempo"]
    major1_minor0 = json_result["mode"]
    time_signature = json_result["time_signature"]
    valence = json_result["valence"]

    
    # Return a dictionary with audio features
    return {
        "duration_m": (duration_ms/60000),
        "energy": energy,
        "tempo": tempo, 
        "mode": major1_minor0,
        "time_signature": time_signature,
        "valence": valence
    }

# Create a list to store audio features for all tracks
audio_features_list = []

# Loop through all items in track_search and get audio features
for track_id in track_search:
    audio_features = get_audio_features(token, track_id)
    
    # Append the results to the audio_features_list
    audio_features_list.append(audio_features)

# Print or use the audio_features_list as needed
for features in audio_features_list:
    print(f"Duration in minutes: {features['duration_m']}")
    print(f"Energy: {features['energy']}")
    print(f"Tempo: {features['tempo']}")
    print(f"Mode: {features['mode']}")
    print(f"Time signature: {features['time_signature']}")
    print(f"Valence: {features['valence']}")
    print("\n")