import requests
import datetime as dt
from statistics import median
import copy
import time

import init_requests
import config


def get_friends_ages(user_id):
    """
    Получаем возраст каждого друга
    """
    friends = init_requests.get_friends(user_id)
    bdates = []
    ages = []

    for each in friends:
        try:
            if len(each['bdate']) < 5:
                bdates.append('NA')
            else:
                bdates.append(each['bdate'])
        except:
            bdates.append('NA')
    
    today = dt.datetime.today()
    for each in bdates:
        try:
            each = dt.datetime.strptime(each, "%d.%m.%Y")
            ages.append(round(((today - each).days/365.25),1))
        except:
            ages.append('NA')

    return ages


def get_friends_friends_ages(user_id):
    """
    Получаем возраст каждого друга
    """
    friends = init_requests.get_friends_ids(user_id)
    friends_friends_median = []

    for each_friend in friends:
        try:
            a = get_friends_ages(each_friend)
            b = [i for i in a if type(i) != str]
            friends_friends_median.append(round(median(b),1))           
        except:
            friends_friends_median.append('NA')
        time.sleep(0.5)

    return friends_friends_median


def get_cities(user_id):
    """
    Получаем города друзей
    """
    friends = init_requests.get_friends(user_id)
    cities = []

    for friend in friends:
        try:
            cities.append(friend['city']['title'])
        except:
            cities.append('NA')

    return cities


def get_hometowns(user_id):
    """
    Получаем родные города друзей
    """
    friends = init_requests.get_friends(user_id)
    hometowns = []

    for friend in friends:
        try:
            hometowns.append(friend['home_town'])
        except:
            hometowns.append('NA')

    for i in range(len(hometowns)):
        if hometowns[i] == '':
            hometowns[i] = 'NA'

    for i in range(len(hometowns)):
        if hometowns[i].isalpha() == False:
            hometowns[i] = 'NA'

    for i in range(len(hometowns)):
        if hometowns[i][0].islower():
            hometowns[i] = hometowns[i].replace(hometowns[i][0], hometowns[i][0].upper())

    return hometowns


def get_friends_count(user_id):
    """
    Получаем количество друзей у каждого друга
    """
    friends = init_requests.get_friends_ids(user_id)
    friends_friends_count = []

    for friend in friends:
        query = (f"https://api.vk.com/method/" +
             f"users.get?" +
             f"fields=counters&" +
             f"user_id={friend}&" +
             f"access_token={config.vk_config['token']}&" +
             f"v=5.122")
        try:
            response = requests.get(url=query).json()['response'][0]['counters']['friends']
            friends_friends_count.append(response)
        except:
            friends_friends_count.append('NA')
        time.sleep(0.5)

    return friends_friends_count


def get_followers_count(user_id):
    """
    Получаем количество подписчиков у каждого друга
    """
    friends = init_requests.get_friends_ids(user_id)
    friends_followers_count = []

    for friend in friends:
        query = (f"https://api.vk.com/method/" +
             f"users.get?" +
             f"fields=counters&" +
             f"user_id={friend}&" +
             f"access_token={config.vk_config['token']}&" +
             f"v=5.122")
        try:
            response = requests.get(url=query).json()['response'][0]['counters']['followers']
            friends_followers_count.append(response)
        except:
            friends_followers_count.append('NA')
        time.sleep(0.5)

    return friends_followers_count


def get_groups_count(user_id):
    """
    Получаем количество групп у каждого друга
    """
    friends = init_requests.get_friends_ids(user_id)
    friends_groups_count = []

    for friend in friends:
        query = (f"https://api.vk.com/method/" +
             f"groups.get?" +
             f"user_id={friend}&" +
             f"access_token={config.vk_config['token']}&" +
             f"v=5.103")
        try:
            response = requests.get(url=query).json()['response']['count']
            friends_groups_count.append(response)
        except:
            friends_groups_count.append('NA')
        time.sleep(0.6)

    return friends_groups_count


def get_inst(user_id):
    """
    Проверяем есть ли у друга ссылка на инсту в профиле
    """
    friends = init_requests.get_friends_ids(user_id)
    inst = []

    for friend in friends:
        query = (f"https://api.vk.com/method/" +
             f"users.get?" +
             f"fields=connections&" +
             f"user_id={friend}&" +
             f"access_token={config.vk_config['token']}&" +
             f"v=5.89")
        response = requests.get(url=query).json()['response']
        if 'instagram' in response[0]:
            inst.append('Yes')
        else:
            inst.append('No')
        time.sleep(0.5)

    return inst


def get_twi(user_id):
    """
    Проверяем есть ли у друга ссылка на твиттер в профиле
    """
    friends = init_requests.get_friends_ids(user_id)
    twi = []

    for friend in friends:
        query = (f"https://api.vk.com/method/" +
             f"users.get?" +
             f"fields=connections&" +
             f"user_id={friend}&" +
             f"access_token={config.vk_config['token']}&" +
             f"v=5.103")
        response = requests.get(url=query).json()['response']
        if 'twitter' in response[0]:
            twi.append('Yes')
        else:
            twi.append('No')
        time.sleep(0.5)

    return twi


def get_heducation(user_id):
    """
    Проверяем есть ли у друга высшее образование
    """
    friends = init_requests.get_friends(user_id)
    heduc = []

    for friend in friends:
        try:
            heduc.append(friend['university_name'])
        except:
            heduc.append('NA')
    
    for i in range(len(heduc)):
        if heduc[i] == '':
            heduc[i] = 'NA'

    return heduc


def get_profile_photos_count(user_id):
    """
    Получаем количество аватарок в профиле
    """
    friends = init_requests.get_friends_ids(user_id)
    photos_count = []       

    for friend in friends:
        query = (f"https://api.vk.com/method/" +
             f"photos.get?" +
             f"album_id=profile&" +
             f"user_id={friend}&" +
             f"access_token={config.vk_config['token']}&" +
             f"v=5.103")
        try:
            response = requests.get(url=query).json()['response']['count']
            photos_count.append(response)
        except:
            photos_count.append('NA')
        time.sleep(0.5)

    return photos_count


if __name__ == '__main__':
    print(get_friends_ages(369826180))
    print(get_friends_friends_ages(369826180))
    print(get_cities(369826180))
    print(get_hometowns(369826180))
    print(get_friends_count(369826180))
    print(get_followers_count(369826180))
    print(get_groups_count(369826180))
    print(get_inst(369826180))
    print(get_twi(369826180))
    print(get_heducation(369826180))
    print(get_profile_photos_count(369826180))
    print(get_groups_members(369826180))
