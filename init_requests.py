import requests

import config


def get_friends_ids(user_id):
    """
    Получаем id друзей
    """
    query = (f"https://api.vk.com/method/" +
             f"friends.get?" +
             f"user_id={user_id}&" +
             f"access_token={config.vk_config['token']}&" +
             f"v=5.122")

    response = requests.get(url=query, timeout=40)
    try:
        ids = response.json()['response']['items']
        return ids
    except:
        return None


def get_friends_names(user_id):
    """
    Получаем полные имена друзей
    """
    query = (f"https://api.vk.com/method/" +
             f"friends.get?" +
             f"fields=bdate&" +
             f"user_id={user_id}&" +
             f"access_token={config.vk_config['token']}&" +
             f"v=5.122")

    response = requests.get(url=query,timeout=40)
    try:
        r = response.json()['response']['items']
        names = [i['first_name'] + ' ' + i['last_name'] for i in r]
        return names
    except:
        return None


def get_friends(user_id):
    """
    Получаем краткую информацию о друзьях
    """
    query = (f"https://api.vk.com/method/" +
             f"friends.get?" +
             f"fields=bdate,city,home_town,education,sex&" +
             f"user_id={user_id}&" +
             f"access_token={config.vk_config['token']}&" +
             f"v=5.122")

    response = requests.get(url=query, timeout=40)
    try:
        return response.json()['response']['items']
    except:
        return None


def get_sex(user_id):
    """
    Получаем пол всех друзей
    """
    friends = get_friends(user_id)
    sex = []

    for friend in friends:
        try:
            if friend['sex'] == 1:
                sex.append('F')
            elif friend['sex'] == 2:
                sex.append('M')
        except:
            sex.append('NA')

    return sex


if __name__ == "__main__":
    print(get_friends_ids(369826180))
    print(get_friends_names(369826180))
    print(get_friends(369826180))
    print(get_sex(369826180))
