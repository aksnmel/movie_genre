#TODO
#More checks and cleansing of the dataset provided
#Better usage of pandas functions

import pandas as pd 

path_movie = '/Users/p770779/Desktop/movies.dat'

df_movies = pd.read_csv(path_movie,sep = '::',engine='python'
                         ,header=None,names=['movie_id','movie_title','genre'])

#To check if there is null values
nan_rows = df_movies[df_movies.isnull().T.any().T]

#Filling with not provided for genre column where there is null
df_movies['genre'] = df_movies['genre'].fillna('not provided')

#Split the gener column based on pipe
df_movies.genre = df_movies.genre.str.split('|')

#Converitng the genre column into list values
genre_list = df_movies['genre'].tolist()

unique_genre_list =[]

#Getting list of unique genre provided in the movies dataset
for x in genre_list:
    for y in x:
        if y not in unique_genre_list:
            unique_genre_list.append(y)

#Below will append each unique genre's as column and mark it 
# #either 0 or 1(if the movie is indicated with that genre)
for j in unique_genre_list:
    df_movies[j] = 0
for i in range(df_movies.shape[0]):
    for j in unique_genre_list:
        if(j in df_movies['genre'].iloc[i]):
            df_movies.loc[i,j] = 1

#Next spliting the title and release year as they are provided in same column
split_values = df_movies['movie_title'].str.split("(",n = 1, expand = True)
df_movies.movie_title = split_values[0]
df_movies['year_of_release'] = split_values[1]
df_movies['year_of_release'] = df_movies.year_of_release.str.replace(')','')


#Cols available in ratings dataset.
r_cols = ['user_id', 'movie_id', 'rating', 'timestamp']

#importing the rating dataset
path_rating = '/Users/p770779/Desktop/ratings.dat'
ratings = pd.read_csv(path_rating,sep='::',header=None,names=r_cols,engine='python')

#aggregating the rating for each movie
df_movie_by_ratings = ratings.groupby(['movie_id'])['rating'].agg('sum')

#Joining the aggregated dataframe with cleansed movie dataframe to have summed ratings across movie
df_left_outer = pd.merge(df_movies,df_movie_by_ratings,on='movie_id',how='left')

#Muitplying each genre with the column with the summed up rating for the movie
#to get the total scores for that genre
for i in list(range(3,29)):
    df_left_outer.iloc[:,i] = df_left_outer.iloc[:,i]*df_left_outer['rating']


genre_in_last_decade = []

#summing up the genre's ratings across year_of_release and get the lsat 10 years for analysis
df_sum_to_get_years = df_left_outer.groupby('year_of_release',as_index=False)[col_list].sum()

#summing up the genre's ratings across year_of_release 
df_sum = df_left_outer.groupby('year_of_release')[col_list].sum()

#obtaining last 10 years list
df_last_10_year = df_sum_to_get_years['year_of_release'].tail(10)

col_list =[]

#Print the last 10 years with top genre for that year
for i in list(range(1,11)):
    genre = df_sum.iloc[-i].idxmax()
    year_of_release = df_last_10_year.iloc[-i]
    print(year_of_release,genre)
