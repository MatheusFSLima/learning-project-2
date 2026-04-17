from services.log_service import add_log
from datetime import datetime
from utils.json_handler import save_data
from services.security import hash_password
from utils.session import (set_current_user,
                           clear_session,
                           get_current_user
                           )


def get_user_by_username(data,username):
    for user in data['users']:
        if user['username'] == username:
            return user
    return None



def register_user(data,username,password):

    if password.strip() == '' or len(password) < 4:
        add_log(data, username, 'REGISTER', 'FAIL')
        return 'INVALID_PASSWORD'

    password_hash = hash_password(password)
    user = {
        'username':username,
        'password':password_hash,
        'attempts': 0,
        'blocked': False,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    data['users'].append(user)
    add_log(data,username,'REGISTER','SUCCESS')
    save_data(data)
    return 'SUCCESS'


def list_users(data):
    if not data['users']:
        return 'EMPTY_LIST'
    return 'USER_LIST'





def unblock_user(data,username):
    if not data['users']:
        return 'EMPTY_LIST'

    user = get_user_by_username(data, username)

    if user is None:
        return 'USER_NOT_FOUND'

    if not user['blocked']:
        return 'USER_NOT_BLOCKED'

    user['blocked'] = False
    user['attempts'] = 0
    add_log(data,username,'UNBLOCK','SUCCESS')
    save_data(data)
    return 'SUCCESS'


def remove_user(data,username):
    if not data['users']:
        return 'EMPTY_LIST'

    user = get_user_by_username(data, username)

    if user is None:
        return 'USER_NOT_FOUND'

    data['users'].remove(user)
    add_log(data,username,'REMOVE','SUCCESS')
    if get_current_user(data):
        clear_session(data)
    save_data(data)

    return 'SUCCESS'



