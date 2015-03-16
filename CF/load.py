__author__ = 'blue'
import math
import time

def load():
    count_data = 0
    count_movie = 0
    filename_data = '../ml-100k/u.data'
    filename_movies = '../ml-100k/u.item'

    user_item_rating = {} #某个用户评价了的电影列表
    item_user_rating = {} #评价了某个电影的用户列表
    with open(filename_data) as file_data:
        for line in file_data:
            count_data += 1
            (userId, itemId, rating, timeStamp) = line.split("\t")
            item_user_rating.setdefault(itemId, {})
            user_item_rating.setdefault(userId, {})
            item_user_rating[itemId][userId] = rating
            user_item_rating[userId][itemId] = rating
        print('data_count : ', count_data)

    movies = {}
    with open(filename_movies, encoding='utf-8') as file_movies:
        for line in file_movies:
            count_movie += 1
            (movie_id, movie_title) = line.split("|")[0:2]
            movies[movie_id] = movie_title
        print('movie_count : ', count_movie)

    return user_item_rating, item_user_rating, movies

def get_user_movies(user_item_rating, user_id):
    '''
    返回指定用户评分的影片id有序列表
    输出指定用户评分影片数量
    '''
    movies = []
    count = 0
    for user in user_item_rating:
        if user is user_id:
            for movie in user_item_rating[user]:
                count += 1
                movies.append(int(movie))
            break
    movies.sort()
    # print('user ', user_id, ' rating ', count, ' movies...')
    return movies

def calcu_user_sim(userId_A, userId_B):
    '''
    计算用户A和用户B的相似度
    '''
    return adjusted_cosine_new(userId_A, userId_B)

def adjusted_cosine_new(userId_A, userId_B):
    '''
    并集，修正的余弦相似性
    :param userId_A: str 用户id
    :param userId_B: str 用户id
    :return:
    '''
    A_movies = get_user_movies(user_item_rating, userId_A)
    B_movies = get_user_movies(user_item_rating, userId_B)
    A_average = average_user(A_movies, userId_A)
    B_average = average_user(B_movies, userId_B)
    union_movies = get_union_movies(A_movies, B_movies)
    a = 0; b = 0; c = 0;
    for movie in union_movies:
        A_movie_rating = user_item_rating.get(userId_A).get(str(movie))
        if A_movie_rating is None:
            A_movie_rating = predict(userId_A, str(movie))
        A_minus = float(A_movie_rating) - A_average
        B_movie_rating = user_item_rating.get(userId_B).get(str(movie))
        if B_movie_rating is None:
            B_movie_rating = predict(userId_B, str(movie))
        B_minus = float(B_movie_rating) - B_average
        a += (A_minus * B_minus)
    for movie in A_movies:
        A_minus = float(user_item_rating[userId_A][str(movie)]) - A_average
        b += (A_minus * A_minus)
    for movie in B_movies:
        B_minus = float(user_item_rating[userId_B][str(movie)]) - B_average
        c += (B_minus * B_minus)
    b = math.sqrt(b)
    c = math.sqrt(c)
    if( b * c == 0):
        return 0
    sim = a / (b * c)
    return sim

def adjusted_cosine(userId_A, userId_B):
    '''
    交集，修正的余弦相似性
    :param userId_A: str 用户id
    :param userId_B: str 用户id
    :return:
    '''
    A_movies = get_user_movies(user_item_rating, userId_A)
    B_movies = get_user_movies(user_item_rating, userId_B)
    A_average = average_user(A_movies, userId_A)
    B_average = average_user(B_movies, userId_B)
    share_movies = get_share_movies(A_movies, B_movies)
    a = 0; b = 0; c = 0;
    for movie in share_movies:
        A_minus = float(user_item_rating[userId_A][str(movie)]) - A_average
        B_minus = float(user_item_rating[userId_B][str(movie)]) - B_average
        a += (A_minus * B_minus)
    for movie in A_movies:
        A_minus = float(user_item_rating[userId_A][str(movie)]) - A_average
        b += (A_minus * A_minus)
    for movie in B_movies:
        B_minus = float(user_item_rating[userId_B][str(movie)]) - B_average
        c += (B_minus * B_minus)
    b = math.sqrt(b)
    c = math.sqrt(c)
    if( b * c == 0):
        return 0
    sim = a / (b * c)
    return sim

def correlation(userId_A, userId_B):
    '''
     交集，根据相似相关性
    :param userId_A: str 用户id
    :param userId_B: str 用户id
    :return:A用户和B用户的相关相似性
    '''
    A_movies = get_user_movies(user_item_rating, userId_A)
    B_movies = get_user_movies(user_item_rating, userId_B)
    A_average = average_user(A_movies, userId_A)
    B_average = average_user(B_movies, userId_B)
    share_movies = get_share_movies(A_movies, B_movies)
    a = 0; b = 0; c = 0;
    for movie in share_movies:
        A_minus = float(user_item_rating[userId_A][str(movie)]) - A_average
        B_minus = float(user_item_rating[userId_B][str(movie)]) - B_average
        a += (A_minus * B_minus)
        b += (A_minus * A_minus)
        c += (B_minus * B_minus)
    b = math.sqrt(b)
    c = math.sqrt(c)
    if( b * c == 0):
        return 0
    sim = a / (b * c)
    return sim

def average_user(movies, userId):
    '''
    计算用户对已评价项目的平均评价
    movies => 用户已评价电影集合
    '''
    sum = 0
    count = 0
    for movie in movies:
        count += 1
        sum += int(user_item_rating[userId][str(movie)])
    # print('count = ', count, ', userId = ', userId, ', sum = ', sum)
    return sum / len(movies)

def get_share_movies(user1_movies, user2_movies):
    '''
    获得user1和user2评价的电影列表交集
    '''
    share = [val for val in user1_movies if val in user2_movies]
    return share

def get_union_movies(user1_movies, user2_movies):
    '''
    获得user1和user2有评价的电影的并集
    '''
    union = list(set(user1_movies).union(set(user2_movies)))
    return union

def get_diff_movies(user1_movies, user2_movies):
    '''
    :param user1_movies:  用户1 评价的电影
    :param user2_movies:  用户2 评价的电影
    :return: 用户2评价而用户1未评价的电影列表
    '''
    diff = list(set(user2_movies).difference(set(user1_movies)))
    return diff

def get_sim_top(userId):
    '''
    :param userId:
    :return: 与userId相似度最高的10个用户id列表
    '''
    sim_list = []
    for user in user_item_rating:
        if user is not userId:
            sim = calcu_user_sim(userId, user)
            sim_dic = {}
            sim_dic['userId'] = user
            sim_dic['sim'] = sim
            sim_list.append(sim_dic)
    # print(len(sim_list), 'user_sim_list => ', sim_list)
    def cmp(s):
        return s['sim']
    top_10 = sorted(sim_list, key= cmp, reverse=True)
    return top_10[0:10]



def get_movie_users(itemId):
    '''
    获得评价指定电影的用户id列表
    并输入多少用户评价了该电影
    '''
    users = []
    count = 0
    for item in item_user_rating:
        if item is itemId:
            for user in item_user_rating[item]:
                count += 1
                users.append(int(user))
            break
    users.sort()
    # print('item ', itemId, ' rating by ', count, ' users...')
    return users

def average_movie(users, itemId):
    '''
    :param users: 对itemId电影评价过的用户id列表
    :param itemId: 电影id
    :return: 所有用户对该电影评分的平均值
    '''
    sum = 0
    count = 0
    for user in users:
        count += 1
        sum += int(item_user_rating[itemId][str(user)])
    # print('count = ', count, ', itemId = ', itemId, ', sum = ', sum)
    if len(users) is 0:
        return 0
    return sum / len(users)

def get_share_users(movie1_users, movie2_users):
    '''
    :param movie1_users: 对电影1评价的用户
    :param movie2_users: 对电影2评价的用户
    :return:交集
    '''
    share = []
    share = [val for val in movie1_users if val in movie2_users]
    return share

def calcu_item_sim(itemId_A, itemId_B):
    '''
    :param itemId_A:
    :param itemId_B:
    :return: 电影A和电影B的相似度，修正的余弦相似性
    '''
    A_users = get_movie_users(itemId_A)
    B_users = get_movie_users(itemId_B)
    A_average = average_movie(A_users, itemId_A)
    B_average = average_movie(B_users, itemId_B)
    share_users = get_share_users(A_users, B_users)
    a = 0; b = 0; c = 0;
    for user in share_users:
        A_minus = float(item_user_rating[itemId_A][str(user)]) - A_average
        B_minus = float(item_user_rating[itemId_B][str(user)]) - B_average
        a += (A_minus * B_minus)
    for user in A_users:
        A_minus = float(item_user_rating[itemId_A][str(user)]) - A_average
        b += (A_minus * A_minus)
    for user in B_users:
        B_minus = float(item_user_rating[itemId_B][str(user)]) - B_average
        c += (B_minus * B_minus)
    b = math.sqrt(b)
    c = math.sqrt(c)
    if (b * c == 0) :
        return 0
    sim = a / (b * c)
    return sim

def get_sim_top_item(itemId):
    '''
    :param itemId:
    :return: 与itemId相似度最高的10个电影id列表
    '''
    sim_list = []
    for movie in item_user_rating:
        if movie is not itemId:
            sim = calcu_item_sim(itemId, movie)
            sim_dic = {}
            sim_dic['itemid'] = movie
            sim_dic['sim'] = sim
            sim_list.append(sim_dic)
    # print(len(sim_list), 'item_sim_list => ', sim_list)
    def cmp(s):
        return s['sim']
    top_10 = sorted(sim_list, key= cmp, reverse=True)
    # print(len(top_10[0:10]), 'top10 => ', top_10[0:10])
    return top_10[0:10]

def predict(userId, itemId):
    '''
    补足用户对并集中未评分电影的评分
    :return:
    '''
    top_10_movie = get_sim_top_item(itemId)
    a = 0
    b = 0
    for movie in top_10_movie:
        userId_rating = user_item_rating.get(userId).get(movie['itemid'])
        if userId_rating is None:
            userId_rating = 0
        a += int(userId_rating)
        b += abs(movie['sim'])
    if b is 0:
        return 0
    return a / b

def recommend(userId, itemId):
    '''
    :param userId:
    :param itemId:
    :return: 预测用户对电影的评分
    '''
    rating = user_item_rating.get(userId).get(itemId)
    if rating is not None :
        return rating
    top_10 = get_sim_top(userId)
    u_average = average_user(get_user_movies(user_item_rating, userId), userId)
    a = 0
    b = 0
    for top in top_10:
        b += abs(top['sim'])
        n_i_average = average_user(get_user_movies(user_item_rating, top['userId']))
        n_i_rating = user_item_rating.get(top['userId']).get(itemId)
        if n_i_rating is None:
            n_i_rating = n_i_average
        a += ( top['sim'] * (n_i_rating - n_i_average) )
    if b is 0:
        return u_average
    rating = u_average + ( a / b )
    return rating


if __name__ == '__main__':
    global user_item_rating, item_user_rating, movies
    user_item_rating, item_user_rating, movies = load()
    start = time.clock()

    # test = get_sim_top_item('2')
    # print(test)
    # movie1_users = get_movie_users('1') #评价过电影1的用户列表
    # print(movie1_users)
    # movie1_average = average_movie(movie1_users, '1') #所有用户对电影1的平均打分
    # print(movie1_average)
    # sim_1_2_movie = calcu_item_sim('1', '2') #电影1和电影2的相似度
    # print('sim movie for 1 and 2 -> ', sim_1_2_movie)
    # top_10_movie = get_sim_top_item('1') #返回与电影1相似度最高的10个电影

    # top_10 = get_sim_top('1') #返回与用户1相似度最高的10个用户
    # sim_1_2 = calcu_user_sim('1', '2') #返回用户1和用户2的相似度
    # print('sim for 1 and 2 -> ', sim_1_2)
    # print(top_10)
    # print(len(top_10), 'top10 => ', top_10)

    # user1_movies = get_user_movies(user_item_rating, '1') #返回用户1评价过的电影列表
    # user2_movies = get_user_movies(user_item_rating, '2') #返回用户2评价过的电影列表
    # diff_movies_1 = get_diff_movies(user1_movies, user2_movies) #和用户2想比，用户1 未评价的电影
    # print(diff_movies_1)
    # share_movies = get_share_movies(user1_movies, user2_movies)   #用户1和用户2评价的电影交集
    # union_movies = get_union_movies(user1_movies, user2_movies)   #并集
    # user1_average = average_user(user1_movies, '1')   #用户1 评价的电影平均分
    # print('user1 => ', user1_movies)
    # print('user1 =R> ', user1_average)
    # print('user2 => ', user2_movies)
    # print('share => ', share_movies)
    # print('union => ', union_movies)
    
    test = recommend('1', '273')
    print(test)

    end = time.clock()
    run_time = round(end - start, 1)
    print('run_time : ', run_time)

