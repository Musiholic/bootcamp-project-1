# Main Branch

Branch Corbin

	This branch signifies what keys are most popular within the listing of the top (non-error) 1500 songs
from Spotify. We found that the majority, by a few hundred songs, of popular songs are in a major key. 
While the key signature of a song is not imperative; there is an obvious love for 'C#/Db' and a dislike for 
'D#/Eb'. The rest of the key signatures remain at a relatively balanced liking. Finally, we find there to be a
strong like for medium to medium-high energy songs. Thus we can conclude that the most popular songs are tending
towards a medium-high energy song in 'C#/Db' Major.


# Main Branch
#From Branch-Joss Investigation
**Do Song Lyric Count/Variety correlate to the popularity of a song?**
For the data, we counted the lyrics of all the songs, and counted the unique lyrics of all the songs. Additionally, those counts were compared to lyric count and unique lyric count for Popular Songs, meaning songs that peaked in the Top 10.
For the lyric count for all songs, the Mean: 335.8233690873923, Median: 332.0, Mode: 0, Variance: 67599.5937877889, Standard Deviation: 259.99921882149744.
(Plots found in Cell 11 of lyrics3.pynb)
For the lyric count of popular songs, the Mean: 366.2063615205586, Median: 377.0, Mode: 0, Variance: 75441.62974210842, Standard Deviation: 274.66639718412665.
(Plots found in Cell 14 of lyrics3.pynb)
This indicates that popular music actually has a higher lyric count than music as a whole. This could be due to the genre of songs popularized in todays culture, however, that research was not done here.
For unique lyrics, for all songs, Mean: 135.8066643221382, Median: 123.0, Mode: 0, Variance: 12301.276871084097, Standard Deviation: 110.91112149412292.
((Plots found in Cell 17 of lyrics3.pynb)
For unique lyrics, for popular songs, Mean: 148.58494957331266, Median: 139.0, Mode: 0, Variance: 13549.41533231497, Standard Deviation: 116.40195587839136.
Again, popular music is using more unique words, than songs as a whole.
Caveat to this finding, I kept in songs with 0 lyrics, some of these are 0 because of error, some are 0 because they have no lyrics, it is possible that a fully cleaned datasetwould modidy these findings. For this reason, the distribution tables are all bimodal.
This distribution charts of the formerly discussed data can be found here:
(Plots found in Cell 12 of lyrics3.pynb)
(Plots found in Cell 15 of lyrics3.pynb)
(Plots found in Cell 18 of lyrics3.pynb)
(Plots found in Cell 21 of lyrics3.pynb)
For lyric count, for all songs, they were slightly positively correlated (0.0207) to days on the chart. The unique word count, for all songs, had a slightly negative correlation (-0.003) to days on the chart. This indicates that the amount of words is more important to song popularity than variety.
(Plots found in Cell 22 of lyrics3.pynb)
(Plots found in Cell 23 of lyrics3.pynb)
Both total words, and unique words, for all songs have a slight positive correlation in regard to total streams of songs, at 0.022 and 0.003.
**Do the most popular artists have more Top 10 hits than other artists?**
Unlike the flash in the pan One-Hit-Wonder artists, the biggest artists in the world have multiple Top 10 hits. The Total Streams of an Arist is correlated positively (0.568) to the average position of their songs. Additionally, the higher amount of Top 10 songs an artist has, strongly positively correlates (0.922) to the amount of Total Streams of an Artist.
(Plots found in Cell 29 of lyrics3.pynb) This chart shows a negative trend, but that is because a lower number indicates a higher chart position, so the negative correlation is actually a positive correlation.
(Plots found in Cell 33 of lyrics3.pynb)
Additionally, in both cases, there is a p-value of 0.0, which shows that the more hit songs an artist has, the more total streams the artist will have.

# Branch Aaron
- Used api to retrieve lyrics for the top 11000 streamed songs. These were used to analyze lyric data.
- Do the individual words in a song effect its popularity?
	- By only looking at notable words (not common words). 
	- Looking at the top 5 notable words in each song, I analyzed the statistics of the individual words.
	- "Love" is the most popular notable word. (top_lyrics.png)
	- Songs that contain "Holiday" have the highest average streams. (top_streaming_words.png)
 - # Felix Ologo-Gyan
 - Do songs grow quickly with trends in terms of popularity
 - The dataset was used to look at the relationships of the various variables in the columns and compared in pairs. To see how trends and staying on the chart affect the songs popularity scatter plots for correlation and regression to ascertain the findings were plotted. A correlation value of 0.57 means it is a ‘’positive moderate correlation’’ for Days against top ten chart songs and a none or very weak regression value of 0.0947. 
 - The plots also show how songs popularity are when they first get on the list and how trends fall with days going by.
 - A summary statistics was done on the artist peak streams after merging main data with the lyrics to see the mean, median, variance, standard deviation
 - Bar chart to show the Artist and their peak strems on the music chart
