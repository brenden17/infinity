import pandas as pd
import matplotlib.pyplot as plt

def get_data():
    data_dir = '/media/main/data/source/pydata-book-master/ch02/movielens/'

    unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
    users = pd.read_table(data_dir+'users.dat', sep='::', header=None,
names=unames)

    unames = ['user_id', 'movie_id', 'rating', 'timestamp']
    ratings = pd.read_table(data_dir+'ratings.dat', sep='::', header=None, names=unames)

    unames = ['movie_id', 'title', 'genres']
    movies = pd.read_table(data_dir+'movies.dat', sep='::', header=None, names=unames)

    data = pd.merge(pd.merge(ratings, users), movies)

    return data 

def get_top():
    data = get_data()
    mean_ratings = data.pivot_table('rating', rows='title', cols='gender', aggfunc='mean')
    ratings_by_title = data.groupby('title')
    print ratings_by_title

if __name__=='__main__':
    get_top()
