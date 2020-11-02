import random
import pickle
import numpy as np
import pandas as pd
from sklearn.utils import shuffle


totaldf = pd.read_csv("API/data/movies.csv")
totaldf = shuffle(totaldf)
totaldf.drop(['Unnamed: 0'], axis=1, inplace=True)
totaldf['genres'].fillna("", inplace=True)
totaldf['tagline'].fillna("", inplace=True)
totaldf['summary'].fillna("", inplace=True)
totaldf['imdbRating'].fillna(random.randint(0,10), inplace=True)
totaldf['imdbRating'] = totaldf['imdbRating']/2


def popular():
    rating = totaldf.copy()
    json = (
        rating.sort_values(
            ['imdbRating', 'releaseDate'],
            ascending=False)[
        0:10])
    return json


def recent():
    recent = totaldf.copy()
    json = (
        recent.sort_values(
            'releaseDate',
            ascending=False)[
        0:10]).to_dict(orient="records")
    return json


def category_sort(category, type, num="all"):

    type = type.lower()
    movies = totaldf.copy()
    movies = movies[movies[category] == type]
    if num == "all":
        json = (movies.sort_values('releaseDate', ascending=False))
        json = genres("all", json, 25, "defined")
        return json['movies']
    else:
        json = (movies.sort_values('releaseDate', ascending=False))[0:num].to_dict(orient="records")
    return json


def genres(genre, dataset, num=18, data="undefined"):
    movies = {"movies" : []}
    if data ==  "undefined":
        genre_movies = totaldf.copy()
    else:
        genre_movies = dataset
    genre_movies['genres'] = genre_movies['genres'].apply(lambda x: x.split('|'))
    gens = []
    for lis in list(genre_movies['genres']):
        for item in lis:
            gens.append(item)

    print(len(list(set(gens))))
    if data=="defined":
        gens = random.sample(list(set(gens)), 20)
    else:
        gens = random.sample(list(set(gens)), 9)

    for gen in gens:
        row = 0
        movie = {}
        rows = []
        for genre in genre_movies['genres']:
            if gen in genre:
                rows.append(row)
            row += 1
            if len(rows) == num:
                movie["gen"] = gen
                movie["details"] = genre_movies.iloc[rows].to_dict(orient="records")
                movies["movies"].append(movie)
                break
    return movies

def video_links(imdbId):

    links_df = pd.read_csv("API/data/youtube_links.csv")
    link = links_df['youtubeId'][links_df['imdbId'] == imdbId].to_string(index=False)
    if link == 'Series([], )':
        with open('API/data/links.pkl', 'rb') as file:
            links = pickle.load(file)
        link = random.choice(links)
    else:
        link = links_df['youtubeId'][links_df['imdbId'] == imdbId].to_string(index=False)


    return {"id" : link}

