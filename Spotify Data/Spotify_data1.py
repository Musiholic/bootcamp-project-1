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

#searching for track id using track name and artists name, doing this because there are repeat song titles in the csv
def search_for_track(token, track_name, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={track_name} {artist_name}&type=track&limit=1"

    try:
        query_url = url + query
        result = get(query_url, headers=headers)
        json_result = json.loads(result.content)["tracks"]["items"]
    except requests.exceptions.SSLError as e:
        print(f"SSL Error: {e}")
    except KeyError as k:
        print(f"error {k}")

    if len(json_result) == 0:
        print(f"No track with the name '{track_name}' by '{artist_name}' found.")
        return None
    else:
        return json_result[0]["id"]  # Return the track ID

# Iterate through all items in the song list and search for each track ID
for track_name, artist_name in zip(song, artist):
    # Search for track ID
    track_id = search_for_track(token, track_name, artist_name)

    if track_id:
        track_search.append(track_id)
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
    key = json_result["key"]
    
    # Return a dictionary with audio features
    return {
        "duration_s": (duration_ms/1000),
        "energy": energy,
        "tempo": tempo, 
        "mode": major1_minor0,
        "time_signature": time_signature,
        "valence": valence,
        "key": key
    }

# Create a list to store audio features for all tracks
audio_features_list = []

# Loop through all items in track_search and get audio features
for track_id in track_search:
    audio_features = get_audio_features(token, track_id)
    
    # Append the results to the audio_features_list
    audio_features_list.append(audio_features)

# # Check if song_artist and combined_audio lists have the same length
# if len(track_search) == len(song) == len(artist) == len(audio_features_list):
#     combined_data = []

#     for i in range(len(song)):
#         # Create a new dictionary for each entry
#         combined_dict = {
#             "song": song[i],
#             "artist": artist[i],
#             "track_id": track_search[i],
#             "duration_s": audio_features_list[i]["duration_s"],
#             "energy": audio_features_list[i]["energy"],
#             "tempo": audio_features_list[i]["tempo"], 
#             "mode": audio_features_list[i]["mode"],
#             "time_signature": audio_features_list[i]["time_signature"],
#             "valence": audio_features_list[i]["valence"],
#             "key": audio_features_list[i]["key"]
#         }

#         combined_data.append(combined_dict)

#     # Print or use the combined_data list as needed
#     for entry in combined_data:
#         print()
# else:
#     print("Lists must have the same length for this operation.")

# Set the chunk size
chunk_size = 500

# Initialize a list to store all combined data
all_combined_data = []

# Open the CSV file in write mode
csv_file_path = 'spotify_data_all.csv'
with open(csv_file_path, 'w', newline='') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)

    # Write the header row
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

            # Print or use the combined_data list as needed for each chunk
            for entry in combined_data:
                print(entry)
        else:
            print("Lists must have the same length for this operation.")

# Optionally, you can save all_combined_data to a CSV file after the loop
with open('spotify_data_all_combined.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(header_row)
    for entry in all_combined_data:
        row_values = [entry[key] for key in header_row]
        csv_writer.writerow(row_values)

print(f"CSV file '{csv_file_path}' has been created.")