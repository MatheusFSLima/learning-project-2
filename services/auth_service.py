from services.user_service import get_user_by_username
from services.log_service import add_log
from utils.json_handler import save_data
from services.security import hash_password
from utils.session import (get_current_user,
                           set_current_user,
                           clear_session
                            )
from constants import (USER_NOT_FOUND,
                       SUCCESS,
                       NO_USER_LOGGED,
                       INVALID_USERNAME,
                       USERNAME_ALREADY_EXISTS,
                       BLOCKED,
                       INVALID_PASSWORD,
                       EMPTY_LIST,
                       OK,
                       LOGIN,
                       FAIL,
                       LOGOUT,

                       )


def login(data,username,password):


    user = get_user_by_username(data, username)

    if not user:
        return USER_NOT_FOUND,None

    if validate_password(user,password):
        reset_attempts(user)
        set_current_user(data,user)
        add_log(data,user['username'],LOGIN,SUCCESS)
        save_data(data)
        return SUCCESS, None


    result,attempts = handle_failed_attempt(user)
    add_log(data, user['username'], LOGIN, FAIL)
    save_data(data)
    return result, attempts



def logout(data):
    current_user = get_current_user(data)

    if not current_user:
        return NO_USER_LOGGED, None

    add_log(data, current_user['username'], LOGOUT, SUCCESS)
    clear_session(data)
    save_data(data)
    return SUCCESS, None


def validate_password(user,password):
    password_hash = hash_password(password)
    return user['password'] == password_hash

def handle_failed_attempt(user):
        user['attempts'] += 1
        if user['attempts'] >= 3:
            user['blocked'] = True
            return BLOCKED,user['attempts']
        return INVALID_PASSWORD,user['attempts']


def reset_attempts(user):
    user['attempts'] = 0

def validate_username_for_register(data,username):

    user = get_user_by_username(data, username)

    if not username.replace(' ', '').isalpha() or len(username) < 4:
        return INVALID_USERNAME, None

    if user:
        return USERNAME_ALREADY_EXISTS, None

    return OK, None




def validate_username_for_login(data,username):

    if not username.replace(' ', '').isalpha() or len(username) < 4:
        return INVALID_USERNAME, None

    if not data['users']:
        return EMPTY_LIST, None

    user = get_user_by_username(data, username)

    if user is None:
        return USER_NOT_FOUND, None

    if user['blocked']:
        return BLOCKED, None

    return OK, None


def validate_remove_user(data,username):

    if not username.replace(' ', '').isalpha() or len(username) < 4:
        return INVALID_USERNAME, None

    if not data['users']:
        return EMPTY_LIST, None

    user = get_user_by_username(data, username)

    if user is None:
        return USER_NOT_FOUND, None

    return OK, None


def normalize_username(username):
    return username.strip().lower()



def validate_password_for_register(password):
    if password == '' or len(password) < 4:
        return INVALID_PASSWORD, None
    return OK, None
