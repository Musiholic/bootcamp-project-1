#At the time of writing this, this code is only partially functional. The problems left to be fixed in it's functionality are problems dealing with misspellings and different naming conventions.
#importing dependancies
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import csv
import ssl
ssl._create_default_https_context = ssl._create_default_https_context
import time
from requests import get

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

    #url to send auth request to, and required arguments in headers
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

#getting token
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

# Function to make Spotify API request with backoff-retry
def make_spotify_request_with_retry(url, headers):
    max_retries = 3  
    
    for attempt in range(1, max_retries + 1):
        try:
            response = get(url, headers=headers)

            # Check for rate limit exceeded (429 status code)
            if response.status_code == 429:
                # Parse the Retry-After header
                retry_after = int(response.headers.get('Retry-After', 10))  # Default to 10 seconds

                print(f"Rate limit exceeded. Waiting for {retry_after} seconds before retrying (Attempt {attempt}/{max_retries}).")

                # Wait for the specified duration before retrying
                time.sleep(retry_after)

            # Check for other status codes and handle them as needed
            elif response.status_code == 200:
                # Successful response, process it as needed
                return response.json()

            else:
                # Handle other status codes
                print(f"Unexpected status code: {response.status_code}")
                return None

        except Exception as e:
            print(f"An error occurred: {e}")

        # If this is the last attempt, give up
        if attempt == max_retries:
            print(f"Reached maximum number of retries. Request failed.")
            return None

# Modified search_for_track function with backoff-retry
def search_for_track(token, track_name, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={track_name} {artist_name}&type=track&limit=1"

    try:
        query_url = url + query
        json_result = make_spotify_request_with_retry(query_url, headers)

        if json_result is not None and "tracks" in json_result and "items" in json_result["tracks"]:
            track_items = json_result["tracks"]["items"]
        else:
            track_items = []

    except NameError as e:
        print(f"SSL Error: {e}")
        track_items = []

    if len(track_items) == 0:
        print(f"No track with the name '{track_name}' by '{artist_name}' found.")
        return None
    else:
        return track_items[0]["id"]  # Return the track ID

#retrieving the audio features from the spotify api with the previously retrieved track id for each song
def get_audio_features(token, track_id):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)

    # Check for errors in the API response
    if result.status_code != 200:
        print(f"Error getting audio features for track ID {track_id}. Status code: {result.status_code}")
        return None

    try:
        json_result = result.json()
        # Extract relevant audio features
        duration_ms = json_result.get("duration_ms")
        energy = json_result.get("energy")
        tempo = json_result.get("tempo")
        major1_minor0 = json_result.get("mode")
        time_signature = json_result.get("time_signature")
        valence = json_result.get("valence")
        key = json_result.get("key")
        
        # Return a dictionary with audio features
        return {
            "duration_s": (duration_ms/1000) if duration_ms else None,
            "energy": energy,
            "tempo": tempo, 
            "mode": major1_minor0,
            "time_signature": time_signature,
            "valence": valence,
            "key": key
        }
    except KeyError as e:
        print(f"KeyError: {e}")
        return None
    except Exception as e:
        print(f"Error processing audio features: {e}")
        return None

# Set the chunk size
chunk_size = 500

# Initialize a list to store all combined data
all_combined_data = []

# Writing data from the combined spotify api pulled data and the orinal billboard top 10k streamed songs data, into a csv file
csv_file_path = 'spotify_data_all1.csv'
with open(csv_file_path, 'a', newline='') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)

    header_row = ["song", "artist", "track_id", "duration_s", "energy", "tempo", "mode", "time_signature", "valence", "key"]
    csv_writer.writerow(header_row)

    # Loop through the data in chunks
    for start_index in range(0, len(song), chunk_size):
        end_index = start_index + chunk_size

        # Extract the current chunk of data
        current_song_chunk = song[start_index:end_index]
        current_artist_chunk = artist[start_index:end_index]

        # Initialize a list to store track IDs for the current chunk
        current_track_search = []

        # Iterate through the current chunk and search for each track ID
        for track_name, artist_name in zip(current_song_chunk, current_artist_chunk):
            # Search for track ID
            track_id = search_for_track(token, track_name, artist_name)

            if track_id:
                current_track_search.append(track_id)
            else:
                print(f"Track ID not found for '{track_name}' by '{artist_name}'.")

        # Initialize a list to store audio features for the current chunk
        current_audio_features_list = []

        # Loop through all items in current_track_search and get audio features
        for track_id in current_track_search:
            audio_features = get_audio_features(token, track_id)

            # Append the results to the current_audio_features_list
            current_audio_features_list.append(audio_features)

        # Check if current_song_chunk and current_audio_features_list have the same length
        if len(current_track_search) == len(current_song_chunk) == len(current_artist_chunk) == len(current_audio_features_list):
            combined_data = []

            for i in range(len(current_song_chunk)):
                # Create a new dictionary for each entry
                combined_dict = {
                    "song": current_song_chunk[i],
                    "artist": current_artist_chunk[i],
                    "track_id": current_track_search[i],
                    "duration_s": current_audio_features_list[i]["duration_s"],
                    "energy": current_audio_features_list[i]["energy"],
                    "tempo": current_audio_features_list[i]["tempo"],
                    "mode": current_audio_features_list[i]["mode"],
                    "time_signature": current_audio_features_list[i]["time_signature"],
                    "valence": current_audio_features_list[i]["valence"],
                    "key": current_audio_features_list[i]["key"]
                }

                combined_data.append(combined_dict)
                all_combined_data.append(combined_dict)

                # Write the entry to the CSV file
                csv_writer.writerow([combined_dict[key] for key in header_row])

            # Print or use the combined_data list as needed for each chunk
            for entry in combined_data:
                print(entry)
        else:
            print("Lists must have the same length for this operation.")