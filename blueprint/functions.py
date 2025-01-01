from DBConnection import work_with_db
from . import cache, provider

def get_users(flag_for_update_cache):
    cache_key = 'result'
    cached_profile = cache.get(cache_key)

    if cached_profile and not flag_for_update_cache:
        return cached_profile.decode('utf-8')

    sql = provider.get('get_users.sql')
    data_from_db = str(work_with_db(sql))
    cache.setex(cache_key, 3600, data_from_db)

    return data_from_db

def make_response(message, user):
    result = message + '\n' + \
             'u_id: ' + str(user['u_id']) + '\n' + \
             'name: ' + user['name'] + '\n' + \
             'surname: ' + user['surname'] + '\n' + \
             'email: ' + user['email'] + '\n' + \
             'login: ' + user['login'] + '\n' + \
             'hash_password: ' + user['hash_password'] + '\n' \
             'role_id: ' + str(user['role_id'])
    return result







