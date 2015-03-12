__author__ = 'blue'

def load():
    filename_data = '../ml-100k/u.data'
    filename_movies = '../ml-100k/u.item'

    user_item_rating = {}
    with open(filename_data) as file_data:
        for line in file_data:
            (userId, itemId, rating, timeStamp) = line.split("\t")
            user_item_rating[userId] = {}
            user_item_rating[userId][itemId] = rating

    movies = {}
    with open(filename_movies) as file_movies:
        for line in file_movies:
            (movie_id, movie_title) = line.split("|")[0:2]
            movies[movie_id] = movie_title

    return user_item_rating, movies

if __name__ == '__main__':
    uir, movies = load()
    test = uir['449']['120']
    print(test)
    print(movies)
