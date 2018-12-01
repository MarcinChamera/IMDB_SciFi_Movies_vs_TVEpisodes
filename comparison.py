# -*- coding: utf-8 -*-
import pandas as pd
from matplotlib import pyplot as plt

#importing datasets and executing basic operations on them

df1 = pd.read_csv(r"C:\Users\user\Downloads\Datasets\IMDB_title_basics\data.tsv", sep='\t', 
                  dtype={'genres':str, 'startYear':str})

df2 = df1[['tconst', 'primaryTitle', 'genres', 'startYear','titleType']]

df3 = pd.read_csv(r"C:\Users\user\Downloads\Datasets\IMDB_title_ratings\data.tsv", delim_whitespace=True, 
                  dtype={'averageRating':float, 'numVotes':int})

df_SEnumbers = pd.read_csv(r"C:\Users\user\Downloads\Datasets\IMDB_TVSeries\data.tsv", delim_whitespace=True,
                           dtype={'seasonNumber':str, 'episodeNumber':str})
dfs = pd.merge(df2, df3)
df_without_na = dfs.dropna()
dfs2 = pd.merge(dfs, df_SEnumbers)

#creating dataframes for movies and tv episodes, filtering data

movies = df_without_na.drop(df_without_na[df_without_na.titleType != 'movie'].index)
SciFiMovies = movies[movies.genres.str.contains('Sci-Fi') & (movies.numVotes >= 1000) & (movies.averageRating >= 7)]
packed_SFM = SciFiMovies.drop(['tconst', 'genres', 'startYear', 'titleType'], axis=1)
sortedSFM = packed_SFM.sort_values(by='averageRating', ascending=False)
finalSFM = sortedSFM.set_index('primaryTitle')
SFM_rating_count = finalSFM['averageRating'].value_counts().sort_index()

tv_df = pd.merge(df_without_na, df_SEnumbers)
tv_df = tv_df.drop(tv_df[tv_df.titleType == 'tvMovie'].index)
tv_df_without_na = tv_df.drop(tv_df[(tv_df.seasonNumber == r'\N') | (tv_df.episodeNumber == r'\N')].index)
SciFiTV = tv_df_without_na[tv_df_without_na.genres.str.contains('Sci-Fi') & (tv_df_without_na.numVotes >= 1000) & \
          (tv_df_without_na.averageRating >= 7)]
SciFiTV = SciFiTV.drop(['tconst', 'startYear', 'titleType', 'parentTconst', 'genres'], axis=1)
sortedSFTV = SciFiTV.sort_values(by='averageRating', ascending=False)
finalSFTV = sortedSFTV.set_index('primaryTitle')
SFTV_rating_count = finalSFTV['averageRating'].value_counts().sort_index()

#gathering info to show it on plot

SFM_text = ""
for i in range(10):
    SFM_text += "%i. %s avg.rate: %.1f \n" % (i+1, finalSFM.index[i], finalSFM['averageRating'][i])
SFM_final_text = ("Top 10 rated Sci-Fi movies ever:\n") + (SFM_text)

SFTV_text = ""
for i in range(10):
    SFTV_text += "%i. %s (S%s E%s) avg.rate: %.1f \n" % (i+1, finalSFTV.index[i], finalSFTV['seasonNumber'][i], 
    finalSFTV['episodeNumber'][i], finalSFTV['averageRating'][i]) 
SFTV_final_text = ("\nTop 10 rated Sci-Fi episodes ever:\n") + (SFTV_text)

final_text = SFM_final_text + SFTV_final_text

#creating the plot

fig = plt.figure()
ax = fig.add_subplot(111)
x = [x * 0.1 for x in range(70,100)]
y_m = SFM_rating_count
y_tv = SFTV_rating_count
ax.bar(y_m.index, y_m, width=-0.025, align='edge', label='Movies')
ax.bar(y_tv.index, y_tv, width=0.025, align='edge', label='TV Episodes')
ax.legend(loc='upper left', fontsize=15)
ax.set_title("Sci-Fi Movies / TV Episodes from IMDB database with over 1 000 ratings", fontsize=15)
ax.set_xlabel('User rating', fontsize=15)
ax.set_ylabel('Number of movies / TV Episodes which received the rating', fontsize =15)
ax.set_yticks(range(0,90,5))
ax.set_xticks([x*0.1 for x in range(70,100)])
ax.set_xlim(left=6.9, right=10.0)
ax.text(9.23, 38, final_text, color='black', bbox=dict(edgecolor='grey', facecolor='white', 
        boxstyle='round'), fontsize=11)
ax.yaxis.grid(True, linestyle='--')
ax.set_axisbelow(True)

plt.show()

#not used methods, helpful in different scenarios

"""
plt.gcf().subplots_adjust(bottom=1, top=1, left=1, right=1)
ymin, ymax = ax.get_ylim()
xmin, xmax = ax.get_xlim()
print(xmin, xmax, ymin, ymax)
fig.set_tight_layout(False)
"""