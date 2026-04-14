from services.user_service import get_user_by_username
from services.log_service import add_log
from utils.json_handler import save_data
from services.security import hash_password
from ui.ui import get_current_user,get_current_username


def login(data):
    if not data['users']:
        print('Lista de usuários vazia.\n')
        return
    if data['session']['current_user']:
        print ('Login já realizado.\n')
        return

    username = input ('Digite seu nome de usuário: ').strip().title()

    if not username.replace(' ','').isalpha():
        print ('Nome de usuário inválido. \n')
        return

    user = get_user_by_username(data,username)

    if user is None:
        print ('Usuário não cadastrado.\n')
        return
    if user['blocked']:
        print ('Usuário bloqueado.\n')
        return

    while user['attempts'] < 3:
        password = input ('Digite sua senha: ').strip()
        if validate_password(user,password):
            print ('Login realizado com sucesso.\n')
            reset_attempts(user)
            data['session']['current_user'] = user
            add_log(data,username,'LOGIN','SUCCESS')
            save_data(data)
            return
        else:
            handle_failed_attempt(data,user,username)
            save_data(data)

def logout(data):
    current_user = get_current_user(data)
    current_username = get_current_username(data)
    if not current_user:
        print ('Faça login primeiro.\n')
        return

    option = input ('Tem certeza que deseja sair? [S/N]').strip().lower()
    if option == 's':
        add_log(data, current_username, 'LOGOUT', 'SUCCESS')
        data['session']['current_user'] = None
        save_data(data)
        print ('Logout realizado com sucesso.\n')
        return
    else:
        print ('Usuário continua logado.\n')
        add_log(data,current_username,'LOGOUT','FAIL')
        save_data(data)
        return




def validate_password(user,password):
    password_hash = hash_password(password)
    return user['password'] == password_hash

def handle_failed_attempt(data,user,username):
        user['attempts'] += 1
        add_log(data, username, 'LOGIN', 'FAIL')
        print (f'Senha inválida. Tentativa {user["attempts"]} de 3.')
        if user['attempts'] >= 3:
            user['blocked'] = True
            print ('Usuário bloqueado por tentativas')
            return

def reset_attempts(user):
    user['attempts'] = 0






