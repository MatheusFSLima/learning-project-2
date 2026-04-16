from services.user_service import get_user_by_username
from services.log_service import add_log
from utils.json_handler import save_data
from services.security import hash_password
from utils.session import (get_current_user,
                           set_current_user,
                           clear_session
                            )


def login(data,username,password):
    if not data['users']:
        return 'EMPTY_LIST'

    if get_current_user(data):
        return 'ALREADY_LOGGED'

    if not username.replace(' ','').isalpha():
        return 'INVALID_USERNAME'

    user = get_user_by_username(data,username)

    if user is None:
        return 'USER_NOT_FOUND'
    if user['blocked']:
        return 'BLOCKED'

    if validate_password(user,password):
        reset_attempts(user)
        set_current_user(data,user)
        add_log(data,user['username'],'LOGIN','SUCCESS')
        save_data(data)
        return 'SUCCESS'
    else:
        handle_failed_attempt(data,user,username)
        save_data(data)
        return 'INVALID_PASSWORD'


def logout(data):
    current_user = get_current_user(data)
    if not current_user:
        return 'NO_USER_LOGGED'

    add_log(data, current_user['username'], 'LOGOUT', 'SUCCESS')
    clear_session(data)
    save_data(data)
    return 'SUCCESS'


def validate_password(user,password):
    password_hash = hash_password(password)
    return user['password'] == password_hash

def handle_failed_attempt(data,user,username):
        user['attempts'] += 1
        add_log(data, user['username'], 'LOGIN', 'FAIL')
        print (f'Senha inválida. Tentativa {user["attempts"]} de 3.')
        if user['attempts'] >= 3:
            user['blocked'] = True
            print ('Usuário bloqueado por tentativas')
            return

def reset_attempts(user):
    user['attempts'] = 0






