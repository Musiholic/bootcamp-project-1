#import dependancies 
import os
import pandas as pd

#set csv path
csv_path = os.path.join("bootcamp-project-1","Spotify Data","spotify_data_all.csv")
#read csv into pandas df
audio_analysis_df = pd.read_csv(csv_path, encoding='latin1')

#formatting and printing the average duration of the songs
mean_duration = audio_analysis_df['duration_s'].mean()
mean_duration_m_s = str(int(mean_duration // 60 )) + ":" + str(int(mean_duration % 60))
print(f"Average song length: {mean_duration_m_s}")

#counting the occurence of major and minor in the list
major_minor = audio_analysis_df['mode']
minor = major_minor.value_counts()[0]
major = major_minor.value_counts()[1]
print(f"Songs in a major key {major}")
print(f"Songs in a minor key {minor}")

#binning the energy levels into quartiles and printing final counts of each
energy_level = audio_analysis_df['energy']
bins = [0, 0.25, 0.50, 0.75, 1]
labels = ["low energy","low-medium energy", "high-medium energy", "high-energy"]
audio_analysis_df["Energy Levels"] = pd.cut(energy_level, bins=bins, labels=labels, right=False)
energy_binned = audio_analysis_df["Energy Levels"].value_counts()
print(energy_binned)

#dictionary of key signatures 
key_signatures_dict = { 0:"C",
    1: "C#/Db" ,
    2: "D" ,
    3: "D#/Eb",
    4: "E",
    5: "F",
    6: "F#/Gb",
    7: "G",
    8: "G#/Ab",
    9: "A",
    10: "A#/Bb",
    11: "B"
}

#list of key signatures
key_signature = ["C",
    "C#/Db",
    "D",
    "D#/Eb",
    "E",
    "F",
    "F#/Gb",
    "G",
    "G#/Ab",
    "A",
    "A#/Bb",
    "B"]

#adding column with written out key signature for user ease, counting and printing the counts of each key signature occurence
audio_analysis_df["Key Signature"] = audio_analysis_df["key"].map(key_signatures_dict)
key_signature_count = audio_analysis_df[audio_analysis_df["Key Signature"].isin(key_signature)]["Key Signature"].value_counts()
print(key_signature_count)

#finding and printing the average bpm 
mean_tempo = audio_analysis_df["tempo"].mean()
print(f"Average BPM: {int(mean_tempo)}")

#binning valence into more accessible terms based on quartiles and then printing the counts for each bin
valence = audio_analysis_df["valence"]
bins = [0, .25, .5, .75, 1]
labels = ['highly emotionally negative','emotionally negative', 'emotionally positive', 'highly emotionally positive']
audio_analysis_df["Emotional Rating"] = pd.cut(valence, bins=bins, labels=labels, right=False)
emotional_rating = audio_analysis_df["Emotional Rating"].value_counts()
print(emotional_rating)

#printing counts for each time signature
time_signature = audio_analysis_df["time_signature"]
time_signature_counts_4 = time_signature.value_counts()[4]
time_signature_counts_3 = time_signature.value_counts()[3]
time_signature_counts_5 = time_signature.value_counts()[5]
time_signature_counts_1 = time_signature.value_counts()[1]
print(f"Time signature 1/4 count: {time_signature_counts_1}")
print(f"Time signature 3/4 count: {time_signature_counts_3}")
print(f"Time signature 4/4 count: {time_signature_counts_4}")
print(f"Time signature 5/4 count: {time_signature_counts_5}")

#section used to create the csv file merged_audio_charts.csv
# top_10k_path = os.path.join("bootcamp-project-1","Resources","top_10k_streamed_songs.csv")
# top_10k_df = pd.read_csv(top_10k_path)

# merged_df = pd.merge(audio_analysis_df, top_10k_df, how='left', left_on=['song', 'artist'], right_on=['Song Name', 'Artist Name'])
# merged_df_drop_duplicates = merged_df.drop_duplicates(subset=['song','artist'])
# # Display the merged DataFrame

# merged_df_drop_duplicates.to_csv("merged_audio_chart.csv", index=False)
