import csv
import os
import pandas as pd

csv_path = os.path.join("..","group_challenge_1","spotify_data_all.csv")

audio_analysis_df = pd.read_csv(csv_path, encoding='latin1')

mean_duration = audio_analysis_df['duration_s'].mean()
mean_duration_m_s = str(int(mean_duration // 60 )) + ":" + str(int(mean_duration % 60))
print(f"Average song length: {mean_duration_m_s}")

major_minor = audio_analysis_df['mode']
minor = major_minor.value_counts()[0]
major = major_minor.value_counts()[1]
print(f"Songs in a major key {major}")
print(f"Songs in a minor key {minor}")

energy_level = audio_analysis_df['energy']
bins = [0, 0.25, 0.50, 0.75, 1]
labels = ["low energy","low-medium energy", "high-medium energy", "high-energy"]
audio_analysis_df["Energy Levels"] = pd.cut(energy_level, bins=bins, labels=labels, right=False)
energy_binned = audio_analysis_df["Energy Levels"].value_counts()
print(energy_binned)

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

audio_analysis_df["Key Signature"] = audio_analysis_df["key"].map(key_signatures_dict)
key_signature_count = audio_analysis_df[audio_analysis_df["Key Signature"].isin(key_signature)]["Key Signature"].value_counts()
print(key_signature_count)

mean_tempo = audio_analysis_df["tempo"].mean()
print(f"Average BPM: {int(mean_tempo)}")

valence = audio_analysis_df["valence"]
bins = [0, .25, .5, .75, 1]
labels = ['highly emotionally negative','emotionally negative', 'emotionally positive', 'highly emotionally positive']
audio_analysis_df["Emotional Rating"] = pd.cut(valence, bins=bins, labels=labels, right=False)
emotional_rating = audio_analysis_df["Emotional Rating"].value_counts()
print(emotional_rating)

time_signature = audio_analysis_df["time_signature"]
time_signature_counts_4 = time_signature.value_counts()[4]
time_signature_counts_3 = time_signature.value_counts()[3]
time_signature_counts_5 = time_signature.value_counts()[5]
time_signature_counts_1 = time_signature.value_counts()[1]
print(f"Time signature 4/4 count: {time_signature_counts_4}")
print(f"Time signature 3/4 count: {time_signature_counts_3}")
print(f"Time signature 5/4 count: {time_signature_counts_5}")
print(f"Time signature 1/4 count: {time_signature_counts_1}")