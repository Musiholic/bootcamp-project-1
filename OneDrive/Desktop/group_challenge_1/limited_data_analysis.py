import csv
import os
import pandas as pd

csv_path = os.path.join("..","group_challenge_1","spotify_data_all.csv")

audio_analysis_df = pd.read_csv(csv_path, encoding='latin1')

mean_duration = audio_analysis_df['duration_s'].mean()
mean_duration_m_s = str(mean_duration // 60 ) + ":" + str(mean_duration % 60)
print(f"Average song length: {mean_duration_m_s}")


major_minor = audio_analysis_df['mode']
minor = major_minor.value_counts()[0]
major = major_minor.value_counts()[1]
print(f"Songs in a major key {major}")
print(f"Songs in a minor key {minor}")

energy_level = audio_analysis_df['energy']
bins = [0, 0.25, 0.50, 0.75, 1]
labels = ["low energy","low-medium energy", "high-medium energy", "high-energy"]
audio_analysis_df["Bins"] = pd.cut(energy_level, bins=bins, labels=labels, right=False)
print(audio_analysis_df["Bins"].value_counts())

