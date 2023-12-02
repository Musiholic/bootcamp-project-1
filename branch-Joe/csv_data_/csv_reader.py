#importing dependancies
import os
import csv

#path to csv
csvpath = os.path.join('bootcamp-project-1','Resources','top_10k_streamed_songs.csv')

#songs and artists in list, songs listed first then associated artist
song_artist = []

with open(csvpath, 'r', encoding='utf-8') as csvfile:

    csvreader = csv.reader(csvfile, delimiter=',')
    
    csv_header = next(csvreader)
    print(f"CSV Header: {csv_header}")

    for row in csvreader:
        song_artist.append(row[2])
        song_artist.append(row[1])

