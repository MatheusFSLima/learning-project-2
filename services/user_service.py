from services.log_service import add_log
from datetime import datetime
from utils.json_handler import save_data
from services.security import hash_password
from utils.session import (clear_session,
                           get_current_user
                           )
from constants import (SUCCESS,
                       USER_LIST,
                       EMPTY_LIST,
                       USER_NOT_FOUND,
                       USER_NOT_BLOCKED,
                       REGISTER,
                       UNBLOCK,
                       REMOVE,
                       OK,
                       INVALID_USERNAME,
                       USERNAME_ALREADY_EXISTS,
                       )

def get_user_by_username(data,username):
    for user in data['users']:
        if user['username'] == username:
            return user
    return None



def register_user(data,username,password):

    validation,_ = validate_username_for_register(data,username)

    if validation != OK:
        return validation,None

    password_hash = hash_password(password)
    user = {
        'username':username,
        'password':password_hash,
        'attempts': 0,
        'blocked': False,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    data['users'].append(user)
    add_log(data,username,REGISTER,SUCCESS)
    save_data(data)
    return SUCCESS, None


def list_users(data):
    if not data['users']:
        return EMPTY_LIST, None
    return USER_LIST, data['users']





def unblock_user(data,username):
    if not data['users']:
        return EMPTY_LIST, None

    user = get_user_by_username(data, username)

    if user is None:
        return USER_NOT_FOUND, None

    if not user['blocked']:
        return USER_NOT_BLOCKED, None

    user['blocked'] = False
    user['attempts'] = 0
    add_log(data,username,UNBLOCK,SUCCESS)
    save_data(data)
    return SUCCESS, None


def remove_user(data,username):

    user = get_user_by_username(data, username)

    if not user:
        return USER_NOT_FOUND, None

    data['users'].remove(user)
    add_log(data,username,REMOVE,SUCCESS)
    if get_current_user(data):
        clear_session(data)
    save_data(data)

    return SUCCESS, None


def validate_username_for_register(data,username):

    user = get_user_by_username(data, username)

    if not username.replace(' ', '').isalpha() or len(username) < 4:
        return INVALID_USERNAME, None

    if user:
        return USERNAME_ALREADY_EXISTS, None

    return OK, None


